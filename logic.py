from bseller import get_delivery, get_intelipost, get_nfe, get_order_bseller
from hub2b import get_order_hub2b_all_ambientes
import json

def buscar_pedido(order_id):
    hub2b_data = get_order_hub2b_all_ambientes(order_id)

    if not hub2b_data:
        return {"erro": "Pedido não encontrado na Hub2b."}

    pedido_hub = hub2b_data[0]["order"]
    ambiente = hub2b_data[0]["ambiente"]

    id_order_bseller = str(pedido_hub["reference"]["id"])
    ir_order_shopee = str(pedido_hub["reference"]["source"])
    status_order = pedido_hub["status"]["status"]

    order_bseller = get_order_bseller(id_order_bseller)
    entregas = order_bseller.get("entregas")
    id_entrega = entregas[0]["idEntrega"] if entregas else None

    shipment_bseller = get_delivery(id_entrega)
    shipment_bseller = json.loads(shipment_bseller.text)
    transportadora = shipment_bseller.get("transportadora")
    nome_transportadora = transportadora.get("nome") if transportadora else None
    id_cotacao = shipment_bseller.get("idCotacao")

    shipment_intelipost = get_intelipost(id_entrega)
    content = shipment_intelipost.get("content")
    link_rastreio = content.get("tracking_url") if content else None

    nfe = get_nfe(id_entrega)
    chave_acesso = nfe.get("chaveAcesso")
    link_nfe = (
    f"https://www.nfe.fazenda.gov.br/portal/consultaRecaptcha.aspx"
    f"?tipoConsulta=resumo&tipoConteudo=XbSeqxE8pl8&chaveAcesso={chave_acesso}"
)

    return {
        "id_cotacao": id_cotacao,
        "id_entrega": id_entrega,
        "link_nfe": link_nfe,
        "link_rastreio": link_rastreio,
        "nome_transportadora": nome_transportadora,
        "order_bseller": id_order_bseller,
        "order_shopee": ir_order_shopee,
        "status_order": status_order,
        "ambiente": ambiente
    }
