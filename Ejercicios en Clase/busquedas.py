import random
import time
import pandas as pd
import matplotlib.pyplot as plt
import logging
random.seed(0)  # Establece la semilla para la reproducibilidad


# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Búsqueda Secuencial
def busqueda_secuencial(lista, objetivo):
    for i, elemento in enumerate(lista):
        if elemento == objetivo:
            return i
    return -1

# Búsqueda Binaria
def busqueda_binaria(lista, objetivo):
    izquierda, derecha = 0, len(lista) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        elemento_medio = lista[medio]
        if elemento_medio == objetivo:
            return medio
        elif objetivo < elemento_medio:
            derecha = medio - 1
        else:
            izquierda = medio + 1
    return -1

# Medir tiempos de ejecución
resultados = {'tamanio': [], 'secuencial': [], 'binaria': []}
tamanos = range(10, 10001, 100)

for tamano in tamanos:
    lista_numeros = sorted([random.randint(1, 10000) for _ in range(tamano)])  # Lista ordenada para búsqueda binaria
    objetivo = 0

    logging.info(f'Procesando lista de tamaño: {tamano}')

    # Medir tiempo de búsqueda secuencial
    logging.info('Comenzando búsqueda secuencial...')
    inicio = time.perf_counter()
    busqueda_secuencial(lista_numeros, objetivo)
    fin = time.perf_counter()
    resultados['secuencial'].append(fin - inicio)
    logging.info(f'Búsqueda secuencial completada en {fin - inicio} segundos.')

    # Medir tiempo de búsqueda binaria
    logging.info('Comenzando búsqueda binaria...')
    inicio = time.perf_counter()
    busqueda_binaria(lista_numeros, objetivo)
    fin = time.perf_counter()
    resultados['binaria'].append(fin - inicio)
    logging.info(f'Búsqueda binaria completada en {fin - inicio} segundos.')

    resultados['tamanio'].append(tamano)

# Crear un DataFrame para los resultados
df = pd.DataFrame(resultados)

# Graficar resultados
plt.figure(figsize=(12, 6))
plt.plot(df['tamanio'], df['secuencial'], label='Búsqueda Secuencial', marker='o')
plt.plot(df['tamanio'], df['binaria'], label='Búsqueda Binaria', marker='x')
plt.xlabel('Tamaño de la Lista')
plt.ylabel('Tiempo de Ejecución (segundos)')
plt.title('Tiempo de Ejecución de Algoritmos de Búsqueda')
plt.legend()
plt.grid(True)
plt.savefig('busquedas.png')


