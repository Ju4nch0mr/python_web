import os
from flask import Flask, send_file, make_response
from pv_model_g import PVModel, main
import matplotlib.pyplot as plt


app = Flask(__name__)

@app.route('/')
def index():
    # Calculate the model PV
    pv = PVModel(4, 3)
    resultados, Vmpp, Impp, P_max = pv.modelo_pv(G=1000, T=273 + 25)

    # Generate P-V curve
    pv_curve = generate_pv_curve(resultados)
    pv_curve_filename = f"pv_curve_{Vmpp}_{Impp}_{P_max}.png"
    pv_curve_path = os.path.join("static", pv_curve_filename)
    pv_curve_url = f"/{pv_curve_filename}"
    pv_curve_response = make_response(send_file(pv_curve_path, mimetype='image/png'))
    pv_curve_response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    pv_curve_response.headers['Pragma'] = 'no-cache'
    pv_curve_response.headers['Expires'] = '0'
    os.remove(pv_curve_path)  # Remove the file after sending the response

    # Generate I-V curve
    iv_curve = generate_iv_curve(resultados)
    iv_curve_filename = f"iv_curve_{Vmpp}_{Impp}_{P_max}.png"
    iv_curve_path = os.path.join("static", iv_curve_filename)
    iv_curve_url = f"/{iv_curve_filename}"
    iv_curve_response = make_response(send_file(iv_curve_path, mimetype='image/png'))
    iv_curve_response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    iv_curve_response.headers['Pragma'] = 'no-cache'
    iv_curve_response.headers['Expires'] = '0'
    os.remove(iv_curve_path)  # Remove the file after sending the response

    return f"""
    <html>
        <head>
            <title>PV Model Results</title>
        </head>
        <body>
            <h1>PV Model Results</h1>
            <h2>P-V Curve</h2>
            <img src="{pv_curve_url}" alt="P-V Curve">
            <h2>I-V Curve</h2>
            <img src="{iv_curve_url}" alt="I-V Curve">
        </body>
    </html>
    """

def generate_pv_curve(resultados):
    # Save the P-V curve as an image
    plt.figure(figsize=(8, 6))
    plt.plot(resultados['Voltaje (V)'], resultados['Potencia (W)'], label='P-V Curve')
    plt.xlabel('Voltage (V)')
    plt.ylabel('Power (W)')
    plt.title('Power-Voltage Curve')
    plt.grid()
    plt.legend()
    pv_curve_path = 'static/pv_curve.png'
    plt.savefig(pv_curve_path)
    plt.close()
    return pv_curve_path

def generate_iv_curve(resultados):
    # Save the I-V curve as an image
    plt.figure(figsize=(8, 6))
    plt.plot(resultados['Corriente (A)'], resultados['Voltaje (V)'], label='I-V Curve')
    plt.xlabel('Current (A)')
    plt.ylabel('Voltage (V)')
    plt.title('Current-Voltage Curve')
    plt.grid()
    plt.legend()
    iv_curve_path = 'static/iv_curve.png'
    plt.savefig(iv_curve_path)
    plt.close()
    return iv_curve_path

if __name__ == '__main__':
    main()
    app.run(debug=True)