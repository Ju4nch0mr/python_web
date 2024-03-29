from flask import Flask, render_template_string
import numpy as np
from scipy.optimize import fsolve
import pandas as pd

app = Flask(__name__)

@app.route('/')

class PVModel:
    """
    Clase para el modelo de un panel fotovoltaico.
    """

    def __init__(self, num_panels_series, num_panels_parallel):
        self.R_sh = 545.82  # Resistencia en paralelo
        self.k_i = 0.037  # Coeficiente de temperatura
        self.T_n = 298  # Temperatura de referencia
        self.q = 1.60217646e-19  # Carga del electrón
        self.n = 1.0  # Factor de idealidad
        self.K = 1.3806503e-23  # Constante de Boltzmann
        self.E_g0 = 1.1  # Energía de banda prohibida
        self.R_s = 0.39  # Resistencia en serie
        self.num_panels_series = num_panels_series  # Número de paneles en serie
        self.num_panels_parallel = num_panels_parallel  # Número de paneles en paralelo
        self.I_sc = 9.35 * num_panels_parallel  # Corriente de cortocircuito
        self.V_oc = 47.4 * num_panels_series  # Voltaje de circuito abierto
        self.N_s = 72 * num_panels_series  # Número de células en serie

    def validate_inputs(self, G, T):
        """
        Validar los valores de irradiancia y temperatura.
        :param G:  Irradiancia (W/m²)
        :param T:  Temperatura (K)
        :return:  None
        """
        if not isinstance(G, (int, float)) or G <= 0:
            raise ValueError("La irradiancia (G) debe ser un número positivo.")
        if not isinstance(T, (int, float)) or T <= 0:
            raise ValueError("La temperatura (T) debe ser un número positivo.")
        if not isinstance(self.num_panels_series, int) or self.num_panels_series <= 0:
            raise ValueError("El número de paneles en serie debe ser un entero positivo.")
        if not isinstance(self.num_panels_parallel, int) or self.num_panels_parallel <= 0:
            raise ValueError("El número de paneles en paralelo debe ser un entero positivo.")

    def modelo_pv(self, G, T):
        """
        Modelo de un panel fotovoltaico.
        :param G:  Irradiancia (W/m²)
        :param T:  Temperatura (K)
        :return:  DataFrame con los resultados, voltaje, corriente y potencia máximos
        """
        # Validar los valores de irradiancia y temperatura
        self.validate_inputs(G, T)
        # Cálculo de I_rs: corriente de saturación inversa
        I_rs = self.I_sc / (np.exp((self.q * self.V_oc) / (self.n * self.N_s * self.K * T)) - 1)
        # Cálculo de I_o: corriente de saturación inversa
        I_o = I_rs * (T / self.T_n) * np.exp((self.q * self.E_g0 * (1 / self.T_n - 1 / T)) / (self.n * self.K))
        # Cálculo de I_ph: corriente fotogenerada
        I_ph = (self.I_sc + self.k_i * (T - 298)) * (G / 1000)
        # Creación de un vector de voltaje desde 0 hasta V_oc con 1000 puntos
        Vpv = np.linspace(0, self.V_oc, 1000)
        # Inicialización de vectores de corriente y potencia
        Ipv = np.zeros_like(Vpv)
        Ppv = np.zeros_like(Vpv)

        # Función para la ecuación del modelo PV
        def f(I, V):
            return (I_ph - I_o * (np.exp((self.q * (V + I * self.R_s)) / (self.n * self.K * self.N_s * T)) - 1) -
                    (V + I * self.R_s) / self.R_sh - I)
        # Cálculo de la corriente para todo el array de voltaje usando fsolve y vectorización
        Ipv = fsolve(f, self.I_sc * np.ones_like(Vpv), args=(Vpv))
        Ppv = Vpv * Ipv  # Cálculo vectorizado de la potencia

        # Creación de un DataFrame con resultados
        resultados = pd.DataFrame({'Corriente (A)': Ipv, 'Voltaje (V)': Vpv, 'Potencia (W)': Ppv})
        # Encontrar el punto de máxima potencia
        max_power_idx = resultados['Potencia (W)'].idxmax()
        Vmpp = resultados.loc[max_power_idx, 'Voltaje (V)']
        Impp = resultados.loc[max_power_idx, 'Corriente (A)']
        P_max = resultados.loc[max_power_idx, 'Potencia (W)']
        return resultados, Vmpp, Impp, P_max

def print_results_table(pv, G, T, resultados, Vmpp, Impp, P_max):
    """
    Print a results table.
    :param pv: PVModel object
    :param G: Irradiancia (W/m²)
    :param T: Temperatura (K)
    :param resultados: DataFrame with the results
    :param Vmpp: Voltage at maximum power point (V)
    :param Impp: Current at maximum power point (A)
    :param P_max: Maximum power (W)
    :return: None
    """
    print(f"Results for {pv.num_panels_parallel} panels in parallel and {pv.num_panels_series} panels in series")
    print(f"Irradiancia: {G} W/m², Temperatura: {T} K")
    print("\n|-----------------------------------------------------------------------------|")
    print("|                                Resultados                                   |")
    print("|-----------------------------------------------------------------------------|")
    print(f"| Corriente de cortocircuito (Isc): {pv.I_sc:.2f} A                           |")
    print(f"| Voltaje de circuito abierto (Voc): {pv.V_oc:.2f} V                         |")
    print(f"| Corriente a punto de máxima potencia (Imp): {Impp:.2f} A                   |")
    print(f"| Voltaje a punto de máxima potencia (Vmp): {Vmpp:.2f} V                     |")
    print(f"| Potencia máxima (Pmax): {P_max:.2f} W                                     |")
    print("|-----------------------------------------------------------------------------|")
    print("|                              Datos de la simulación                          |")
    print("|-----------------------------------------------------------------------------|")
    print(resultados.to_string(index=False))
    print("|-----------------------------------------------------------------------------|")

def main():
    # Crear un objeto de la clase PVModel
    pv = PVModel(4, 3)
    # Calcular el modelo PV
    resultados, Vmpp, Impp, P_max = pv.modelo_pv(G=1000, T=273+25)
    print_results_table(pv, G=1000, T=273+25, resultados=resultados, Vmpp=Vmpp, Impp=Impp, P_max=P_max)

if __name__ == "__main__":
    main()

    pv = PVModel(4, 3)
    resultados, Vmpp, Impp, P_max = pv.modelo_pv(G=10, T=273+25)
    html = print_results_table(pv, G=1000, T=273+25, resultados=resultados, Vmpp=Vmpp, Impp=Impp, P_max=P_max)
    

def print_results_table(pv, G, T, resultados, Vmpp, Impp, P_max):
    # Code from the original file goes here
    # ...

    html = f"""
    <html>
        <head>
            <title>PV Model Results</title>
        </head>
        <body>
            <h1>Results for {pv.num_panels_parallel} panels in parallel and {pv.num_panels_series} panels in series</h1>
            <p>Irradiancia: {G} W/m², Temperatura: {T} K</p>
            <table border="1">
                <tr>
                    <th>Corriente de cortocircuito (Isc)</th>
                    <th>Voltaje de circuito abierto (Voc)</th>
                    <th>Corriente a punto de máxima potencia (Imp)</th>
                    <th>Voltaje a punto de máxima potencia (Vmp)</th>
                    <th>Potencia máxima (Pmax)</th>
                </tr>
                <tr>
                    <td>{pv.I_sc:.2f} A</td>
                    <td>{pv.V_oc:.2f} V</td>
                    <td>{Impp:.2f} A</td>
                    <td>{Vmpp:.2f} V</td>
                    <td>{P_max:.2f} W</td>
                </tr>
            </table>
            <h2>Simulation Data</h2>
            <table border="1">
                {resultados.to_html(index=False)}
            </table>
        </body>
    </html>
    """
    return html

if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)