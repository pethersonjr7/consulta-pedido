from flask import Flask, render_template, request
from logic import buscar_pedido
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    erro = None

    if request.method == 'POST':
        order_id = request.form.get('order_id')
        try:
            resultado = buscar_pedido(order_id)

            # Verifica se os campos estão todos vazios, nulos ou "-"
            if not resultado:
                erro = "Pedido não encontrado"
            else:
                campos = [
                    resultado.get("id_cotacao"),
                    resultado.get("id_entrega"),
                    resultado.get("link_nfe"),
                    resultado.get("link_rastreio"),
                    resultado.get("nome_transportadora"),
                    resultado.get("order_bseller"),
                    resultado.get("order_shopee"),
                    resultado.get("status_order")
                ]

                if all(not c or str(c).strip() == "-" for c in campos):
                    resultado = None
                    erro = "Pedido não encontrado"
                else:
                    # Mapeamento do nome do ambiente
                    ambiente_map = {
                        "salonline": "SNLE",
                        "zakat": "ZAKA"
                    }
                    if "ambiente" in resultado:
                        resultado["ambiente"] = ambiente_map.get(
                            resultado["ambiente"], resultado["ambiente"]
                        )

        except Exception as e:
            erro = "Erro ao buscar pedido: " + str(e)

    return render_template('index.html', resultado=resultado, erro=erro)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
