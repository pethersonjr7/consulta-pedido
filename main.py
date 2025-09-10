from hub2b import get_order_hub2b_all_ambientes
from bseller import get_order_bseller_all_ambientes

def buscar_pedido(order_id):
    hub2b_data = get_order_hub2b_all_ambientes(order_id)
    bseller_data = get_order_bseller_all_ambientes(order_id)

    return {
        "hub2b": hub2b_data,
        "bseller": bseller_data
    }


if __name__ == "__main__":
    order_id = input("Digite o número do pedido: ")
    resultado = buscar_pedido(order_id)

    for origem, pedidos in resultado.items():
        print(f"\n=== {origem.upper()} ===")
        for r in pedidos:
            print(f"[{r['ambiente']}]")
            print(r["order"])
