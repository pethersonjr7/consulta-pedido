import requests
from auth_hub2b import get_token_hub2b
from config import CONFIG

CANAIS = ["bseller", "shopee", "tiktokshop", "magazineluiza"]

def get_order_hub2b_all_ambientes(order_id):
    results = []

    for env in CONFIG['hub2b']:
        try:
            token = get_token_hub2b(env)
            for canal in CANAIS:
                url = f"https://rest.hub2b.com.br/Orders/{canal}/{order_id}?access_token={token}"
                resp = requests.get(url)

                if resp.status_code == 200:
                    results.append({
                        "ambiente": env,
                        "canal": canal,
                        "source": "hub2b",
                        "order": resp.json()
                    })
                    break  # não precisa tentar os outros canais se já encontrou
        except Exception as e:
            print(f"[HUB2B][{env}] Erro: {e}")

    return results
