# ejercicio 1: 
def leer_poema():
    with open("Ejercicios Módulo 2 Temas 1 y 2/Modulo 5/poema.txt", "r") as archivo:
        for linea in archivo:
            print(linea, end="")

leer_poema()

#ejercicio 2:

def contar_lineas():
    with open("Ejercicios Módulo 2 Temas 1 y 2/Modulo 5/historia.txt", "r") as archivo:
        return len(archivo.readlines())

print(contar_lineas())

#ejercicio 3:
def contar_palabras():
    with open("Ejercicios Módulo 2 Temas 1 y 2/Modulo 5/archivo.txt", "r") as archivo:
        return len(archivo.read().split())

print(contar_palabras())

#ejercicio 4:
def buscar_palabra():
    with open("Ejercicios Módulo 2 Temas 1 y 2/Modulo 5/notas.txt", "r") as archivo:
        contenido = archivo.read()
        return contenido.lower().count("el")

print(f"La palabra 'el' aparece {buscar_palabra()} veces.")

#ejercicio 5:
def display_words():
    with open("Ejercicios Módulo 2 Temas 1 y 2/Modulo 5/story.txt", "r") as archivo:
        palabras = archivo.read().split()
        cortas = [palabra for palabra in palabras if len(palabra) < 4]
        print(cortas)

display_words()

#ejercicio 6:
def hash_display():
    with open("Ejercicios Módulo 2 Temas 1 y 2/Modulo 5/materia.txt", "r") as archivo:
        contenido = archivo.read().strip()
        print("#".join(contenido))

hash_display()

#ejercicio 7:
import string

def generar_archivos():
    for letra in string.ascii_uppercase:
        with open(f"{letra}.txt", "w") as archivo:
            archivo.write(f"Contenido del archivo {letra}.txt")

generar_archivos()

#ejercicio 8
def agregar_texto(texto):
    with open("Ejercicios Módulo 2 Temas 1 y 2/Modulo 5/python.txt", "a") as archivo:
        archivo.write(texto + "\n")
    with open("Ejercicios Módulo 2 Temas 1 y 2/Modulo 5/python.txt", "r") as archivo:
        print(archivo.read())

agregar_texto("Hola, Texto nuevo")

#ejercicio 9:

from collections import Counter

def frecuencia_palabras():
    with open("Ejercicios Módulo 2 Temas 1 y 2/Modulo 5/archivo.txt", "r") as archivo:
        palabras = archivo.read().split()
        return Counter(palabras)

print(frecuencia_palabras())

#ejercicio 10

import os

def existe_archivo(ruta):
    return os.path.isfile(ruta)

print(existe_archivo("Ejercicios Módulo 2 Temas 1 y 2/Modulo 5/archivo.txt")) 