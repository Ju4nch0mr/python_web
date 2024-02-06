import numpy as np
from scipy.optimize import fsolve
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request

app = Flask(__name__)

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
        self.validate_inputs(G, T)
        I_rs = self.I_sc / (np.exp((self.q * self.V_oc) / (self.n * self.N_s * self.K * T)) - 1)
        I_o = I_rs * (T / self.T_n) * np.exp((self.q * self.E_g0 * (1 / self.T_n - 1 / T)) / (self.n * self.K))
        I_ph = (self.I_sc + self.k_i * (T - 298)) * (G / 1000)
        Vpv = np.linspace(0, self.V_oc, 1000)
        Ipv = np.zeros_like(Vpv)
        Ppv = np.zeros_like(Vpv)

        def f(I, V):
            return (I_ph - I_o * (np.exp((self.q * (V + I * self.R_s)) / (self.n * self.K * self.N_s * T)) - 1) -
                    (V + I * self.R_s) / self.R_sh - I)

        Ipv = fsolve(f, self.I_sc * np.ones_like(Vpv), args=(Vpv))
        Ppv = Vpv * Ipv

        resultados = pd.DataFrame({'Corriente (A)': Ipv, 'Voltaje (V)': Vpv, 'Potencia (W)': Ppv})
        max_power_idx = resultados['Potencia (W)'].idxmax()
        Vmpp = resultados.loc[max_power_idx, 'Voltaje (V)']
        Impp = resultados.loc[max_power_idx, 'Corriente (A)']
        P_max = resultados.loc[max_power_idx, 'Potencia (W)']
        return resultados, Vmpp, Impp, P_max

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        G = float(request.form['G'])
        T = float(request.form['T'])
        num_panels_series = int(request.form['num_panels_series'])
        num_panels_parallel = int(request.form['num_panels_parallel'])

        pv = PVModel(num_panels_series, num_panels_parallel)
        resultados, Vmpp, Impp, P_max = pv.modelo_pv(G, T)

        return render_template('index.html',
                               resultados=resultados.to_html(index=False, justify='center'),
                               Vmpp=Vmpp, Impp=Impp, P_max=P_max, G=G, T=T,
                               num_panels_series=num_panels_series,
                               num_panels_parallel=num_panels_parallel)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)