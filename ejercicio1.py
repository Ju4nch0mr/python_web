import time
import pandas as pd
import matplotlib.pyplot as plt

def funcion1(n):
   return n*(n+1)//2

def funcion2(n):
   suma = 0
   for i in range(1,n+1):
      suma += i
   return suma

lista_numeros = [100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]

tiempos = {'funcion1':[], 'funcion2': []}

# Medir tiempos de ejecucion
for n in lista_numeros:
   inicio = time.perf_counter()
   funcion1(n)
   fin = time.perf_counter()
   diferencia = fin - inicio
   tiempos['funcion1'].append(diferencia)

   inicio = time.perf_counter()
   funcion2(n)
   fin = time.perf_counter()
   diferencia = fin - inicio
   tiempos['funcion2'].append(diferencia)


# Imprimir los tiempos
for i in tiempos:
   print(f"Tiempos de ejecucion de la ({i}):")
   for n, t in zip(lista_numeros, tiempos[i]):
      print(f"n = {n}: {t} segundos")
   print()

# Crear un dataframe
df = pd.DataFrame(tiempos, index=lista_numeros)
df.index.name = "n"
df.reset_index(inplace=True)

# Mostrar el dataframe
print(df)

# Generar una grafica
plt.plot(df['n'], df['funcion1'], label="Suma constante", marker='o')
plt.plot(df['n'], df['funcion2'], label="Suma lineal", marker='x')
plt.xlabel("n (Numero de elementos)")
plt.ylabel("Tiempos de ejecucion (s)")
plt.title("Comparacion del Tiempo de Ejecicion: Suma Lineal vs Suma Constante")
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.grid(True)
plt.savefig('Sumatorias.png')