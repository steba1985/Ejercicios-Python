#ejercicio 1:
import numpy as np

arr = np.array([[1, 2], [3, 4], [5, 6], [7, 8]], dtype=np.uint16)
print("Shape:", arr.shape)
print("Dimensiones:", arr.ndim)
print("Tamaño por elemento (bytes):", arr.itemsize)

#ejercicio 2:
arr = np.arange(100, 200, 10).reshape(5, 2)
print(arr)

#ejercici 3:
sampleArray = np.array([[11, 22, 33], 
                        [44, 55, 66], 
                        [77, 88, 99]]) 

tercera_columna = sampleArray[:, 2]

print(tercera_columna)

#ejercicio 4:

sampleArray = np.array([
    [3, 6, 9, 12],
    [15, 18, 21, 24],
    [27, 30, 33, 36],
    [39, 42, 45, 48],
    [51, 54, 57, 60]
])

elementos_pares = sampleArray[sampleArray % 2 == 0]
elementos_impares = sampleArray[sampleArray % 2 != 0]

print("Elementos pares:", elementos_pares)
print("Elementos impares:", elementos_impares)

#ejercicio 5

arrayOne = np.array([[5, 6, 9], [21, 18, 27]])
arrayTwo = np.array([[15, 33, 24], [4, 7, 1]])

matriz_suma = arrayOne + arrayTwo
matriz_cuadrados = matriz_suma ** 2

print("Matriz suma:\n", matriz_suma)
print("Matriz de cuadrados:\n", matriz_cuadrados)

#ejercicio 6
matriz = np.arange(10, 34).reshape(8, 3)
print("Matriz original:\n", matriz)

submatrices = np.split(matriz, 4, axis=0)  

for i, sub in enumerate(submatrices):
    print(f"Submatriz {i+1}:\n", sub)

#ejercicio 7

sampleArray = np.array([[34, 43, 73], 
                        [82, 22, 12], 
                        [53, 94, 66]])

indices_ordenados = np.argsort(sampleArray[1, :])
array_ordenado_fila = sampleArray[:, indices_ordenados]

print("Array ordenado por la segunda fila:\n", array_ordenado_fila)

indices_ordenados1 = np.argsort(sampleArray[:, 1])
array_ordenado_columna = sampleArray[indices_ordenados1, :]

print("Array ordenado por la segunda columna:\n", array_ordenado_columna)

#ejercicio 8

sampleArray = np.array([
    [34, 43, 73],
    [82, 22, 12],  
    [53, 94, 66]
])

max_eje_0 = np.max(sampleArray, axis=0)
min_eje_1 = np.min(sampleArray, axis=1)

print("Máximo del eje 0 (columnas):", max_eje_0)
print("Mínimo del eje 1 (filas):", min_eje_1)

#ejercicio 9

sampleArray = np.array([[34, 43, 73], 
                        [82, 22, 12], 
                        [53, 94, 66]])  

newColumn = np.array([[10], 
                      [10], 
                      [10]])  

matriz_sin_col2 = np.delete(sampleArray, 1, axis=1)
matriz_final = np.insert(matriz_sin_col2, 1, newColumn.flatten(), axis=1)

print("Matriz final:\n", matriz_final)

