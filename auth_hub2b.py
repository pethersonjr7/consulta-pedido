import requests
import datetime
from config import CONFIG

def get_token_hub2b(env: str):
    cred = CONFIG['hub2b'][env]
    now = datetime.datetime.utcnow()

    if cred['access_token'] and (now - cred['last_refresh']).seconds < 7200:
        return cred['access_token']

    if cred['refresh_token']:
        resp = requests.post(
            'https://rest.hub2b.com.br/oauth2/token',
            json={
                "client_id": cred['client_id'],
                "client_secret": cred['client_secret'],
                "grant_type": "refresh_token",
                "refresh_token": cred['refresh_token']
            },
            headers={"Content-Type": "application/json"}
        )
    else:
        resp = requests.post(
            'https://rest.hub2b.com.br/oauth2/login',
            json={
                "client_id": cred['client_id'],
                "client_secret": cred['client_secret'],
                "grant_type": "password",
                "scope": cred['scope'],
                "username": cred['username'],
                "password": cred['password']
            },
            headers={"Content-Type": "application/json"}
        )

    if resp.status_code == 200:
        data = resp.json()
        cred['access_token'] = data['access_token']
        cred['refresh_token'] = data['refresh_token']
        cred['last_refresh'] = now
        return cred['access_token']
    else:
        raise Exception(f"Erro na autenticação Hub2b ({env}): {resp.text}")
