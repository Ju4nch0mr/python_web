from flask import Flask, request, jsonify
import pickle
import io
import base64
import json
import pv_model

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def calculate_solar_panel_model():
    data = request.get_json()
    num_panels_series = data['numPanelsSeries']
    num_panels_parallel = data['numPanelsParallel']

    pv_model = pv_model.PVModel(num_panels_series, num_panels_parallel)
    resultados, Vmpp, Impp, P_max = pv_model.modelo_pv(G=1000, T=273 + 25)

    resultados_json = json.loads(resultados.to_json(orient='records'))

    # Convert the DataFrame to a base64-encoded string
    buffer = io.StringIO()
    resultados.to_csv(buffer)
    resultados_b64 = base64.b64encode(buffer.getvalue().encode()).decode()

    return jsonify({
        'data': resultados_json,
        'Vmpp': Vmpp,
        'Impp': Impp,
        'Pmax': P_max,
        'resultados_b64': resultados_b64,
    })

if __name__ == '__main__':
    app.run(debug=True)