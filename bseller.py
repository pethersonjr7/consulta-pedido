import requests
from config import CONFIG

def get_order_bseller(order_bseller):
    # Tenta em todos os ambientes disponíveis
    for ambiente in CONFIG["bseller"]:
        api_key = CONFIG["bseller"][ambiente]["api_key"]
        url = f"https://api.bseller.com.br/sac/atendimento/entregas/{order_bseller}"
        headers = {
            "Accept": "*/*",
            "X-Auth-Token": api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    raise Exception("Pedido não encontrado em nenhum ambiente Bseller.")

def get_delivery(id_entrega):
    for ambiente in CONFIG["bseller"]:
        api_key = CONFIG["bseller"][ambiente]["api_key"]
        url = f"https://api.bseller.com.br/entregas/{id_entrega}"
        headers = {
            "Accept": "*/*",
            "X-Auth-Token": api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
    raise Exception("Entrega não encontrada em nenhum ambiente Bseller.")

def get_nfe(id_entrega):
    for ambiente in CONFIG["bseller"]:
        api_key = CONFIG["bseller"][ambiente]["api_key"]
        url = f"https://api.bseller.com.br/entregas/{id_entrega}/nf"
        headers = {
            "Accept": "*/*",
            "X-Auth-Token": api_key
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    return {}

def get_intelipost(id_rastreio):
    api_key = CONFIG.get("intelipost_api_key", "")
    if not api_key:
        return {}
    url = f"https://api.intelipost.com.br/api/v1/shipment_order/{id_rastreio}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "api-key": api_key
    }
    return requests.get(url, headers=headers).json()