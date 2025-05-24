
#ejercicio 1
#Crea una clase Staff con los atributos role, depty
#salary. Crea una clase Profesor que herede de la
#clase anterior y que además tenga como
#atributos nombre y edad. Haz que sea posible
#instanciar un profesor dándole valor a t o d o s los
#a t r i b u t o s .
class Staff:
    def __init__(self, role, dept, salary):
        self.role = role
        self.dept = dept
        self.salary = salary

    def ver(self):
        return f"Role: {self.role}, Department: {self.dept}, Salary: {self.salary}"


class Profesor(Staff):
    def __init__(self, role, dept, salary, nombre, edad):
        super().__init__(role, dept, salary)
        self.nombre = nombre
        self.edad = edad

    def ver(self):
        return (f"Name: {self.nombre}, Age: {self.edad}, "
                f"{super().__str__()}")


profesor = Profesor(role="Docente", dept="Matemáticas", salary=45000, nombre="Juan Pérez", edad=40)
print(profesor.ver)

#ejercicio 2
#Representa el siguiente diagrama con sus clases,
#atributos y métodos correspondientes.
#Cada método display debe imprimir el nombre de
#la clase, atributos y valores de la instancia en ese
#momento. Ejemplo: In
#displaymethodofParent1x=10
class Papa:
    def __init__(self, nombre, apellido):
        self.nombre_p = nombre
        self.apellido_p = apellido

    def display(self):
        print(f"Papa: nombre={self.nombre_p}, apellido={self.apellido_p}")


class Mama:
    def __init__(self, nombre, apellido):
        self.nombre_m = nombre
        self.apellido_m = apellido

    def display(self):
        print(f"Mama: nombre={self.nombre_m}, apellido={self.apellido_m}")


class Hijo(Papa, Mama):
    def __init__(self, nombre, apellido, papa_nombre, papa_apellido, mama_nombre, mama_apellido):
        Papa.__init__(self, papa_nombre, papa_apellido)
        Mama.__init__(self, mama_nombre, mama_apellido)
        self.nombre = nombre
        self.apellido = apellido

    def display(self):
        print(f"Hijo: nombre={self.nombre}, apellido={self.apellido}")
        Papa.display(self)  
        Mama.display(self)  

papa1 = Papa("ARISTIDES", "STEBA")
mama1 = Mama("PETRA", "ARVELAIZ")
hijo1 = Hijo("JEAN", "STEBA", papa1.nombre_p, papa1.apellido_p, mama1.nombre_m, mama1.apellido_m)

hijo1.display()

#ejercicio 3
""" Crea una clase Car que herede de Vehicle y que
sobreescriba los métodos m a x _ s p e e d y
change_gear(). Instancia dos objetos de cada
clase y compruebaque la salida de cada método
e s d i s t i n t a """
class Vehicle:
    def __init__(self, max_speed, num_gears):
        self.max_speed = max_speed
        self.num_gears = num_gears
        self.current_speed = 0
        self.current_gear = 0

    def get_max_speed(self):
        return self.max_speed

    def change_gear(self, gear):
        self.current_gear = gear
        print("Cambio a marcha:", gear)

class Car(Vehicle):
    def __init__(self, max_speed, num_gears, model):
        super().__init__(max_speed, num_gears)  
        self.model = model

    def max_speed(self):
        return super().max_speed()  

    def change_gear(self, gear):
        super().change_gear(gear) 
        print("Cambio de marcha")  

vehicle1 = Vehicle(100, 5)
vehicle2 = Vehicle(120, 6)
car1 = Car(150, 6, "Nisan")
car2 = Car(180, 7, "Jeep")

# Comprobar que la salida de cada método es distinta.
print("Velocidad máxima del vehículo 1:", vehicle1.get_max_speed())
print("Velocidad máxima del coche 1:", car1.get_max_speed())
print("Cambio de marcha del vehículo 1:")
vehicle1.change_gear(3)
print("Cambio de marcha del coche 1:")
car1.change_gear(3)

#ejercicio 4
"""Dadas las siguientes clases con el output de sus
respectivos métodos, crea una interfaz formal
q u e las implemente."""
from abc import ABC, abstractmethod

class data1(ABC):
  def __init__(self):
    pass
  @abstractmethod
  def preprocess_data(self, data, y):
    pass
  @abstractmethod
  def fit(self):
    pass
  @abstractmethod
  def predict(self):
    pass

class data2(ABC):
  def __init__ (self):
    pass
  @abstractmethod
  def preprocess_data(self, data, y):
    pass
  @abstractmethod
  def fit(self):
    pass
  @abstractmethod
  def predict(self):
    pass

class SVM(data1):
  def __init__ (self):
    pass

  def preprocess_data(self, data, y):
    print("Processing data at SVM")

  def fit(self):
    print("Training at SVM")

  def predict(self):
    print("Evaluating at SVM")

class DecisionTree(data2):
  def __init__ (self):
    pass

  def preprocess_data(self, data, y):
    print("Processing data at DecisionTree")

  def fit(self):
    print("Training at DecisionTree")

  def predict(self):
    print("Evaluating at DecisionTree")


svm = SVM()
svm.preprocess_data(data=None, y=None)
svm.fit( )
svm.predict()
dt = DecisionTree()
dt.preprocess_data(data=None, y=None)
dt.fit()
dt.predict()

#ejercicio 5
"""Repite el ejercicio anterior esta vez creando una
interfaz informal."""
class data1_1:
  def __init__(self):
    pass

  def preprocess_data(self, data, y):
    pass

  def fit(self):
    pass

  def predict(self):
    pass

class data2_2:
  def __init__ (self):
    pass

  def preprocess_data(self, data, y):
    pass

  def fit(self):
    pass

  def predict(self):
    pass

class SVM1(data1_1):
  def __init__ (self):
    pass

  def preprocess_data(self, data, y):
    print("Processing data at SVM")

  def fit(self):
    print("Training at SVM")

  def predict(self):
    print("Evaluating at SVM")

class DecisionTree1(data2_2):
  def __init__ (self):
    pass

  def preprocess_data(self, data, y):
    print("Processing data at DecisionTree")

  def fit(self):
    print("Training at DecisionTree")

  def predict(self):
    print("Evaluating at DecisionTree")


svm = SVM1()
svm.preprocess_data(data=None, y=None)
svm.fit( )
svm.predict()
dt = DecisionTree1()
dt.preprocess_data(data=None, y=None)
dt.fit()
dt.predict()

#ejercicio 6
"""Crea una clase virtual llamada Algoritmo con los
atributos nombre, tarea y aprendizaje que sea
s u p e r c l a s e d e la c l a s e B a s e C l a s s i fi e r del
problema anterior. Comprueba con el método
issubclass que Algoritmo es padre de
BaseClassifier."""
class Algoritmo:
    def __init__(self, nombre, tarea, aprendizaje):
        self.nombre = nombre
        self.tarea = tarea
        self.aprendizaje = aprendizaje

    def describir(self):
        print(f"Nombre: {self.nombre}, Tarea: {self.tarea}, Tipo de aprendizaje: {self.aprendizaje}")

class BaseClassifier(Algoritmo):
    def __init__(self, nombre, tarea, aprendizaje, tipo_modelo):
        # Inicializamos la superclase Algoritmo
        super().__init__(nombre, tarea, aprendizaje)
        self.tipo_modelo = tipo_modelo

    def clasificar(self, datos):
        print(f"Clasificando datos con el modelo {self.tipo_modelo}")

es_subclase = issubclass(BaseClassifier, Algoritmo)
print("¿BaseClassifier es subclase de Algoritmo?", es_subclase)

#ejercicio 7

"""Escribe un script en Python para mostrar los
distintos formatos de fecha y hora."""

from datetime import datetime
fecha=datetime.today()
print('Fecha: '+fecha.strftime("%x")+' Hora: '+fecha.strftime("%X"))
print('Año: '+fecha.strftime("%Y"))
print('Mes: '+fecha.strftime("%m"))
print('#Semana del Año: '+fecha.strftime("%W"))
print('Dia de la Semana: '+fecha.strftime("%A"))
print('Dia del Año: '+fecha.strftime("%j"))
print('Dia del Mes: '+fecha.strftime("%d"))
print('Dia de la Semana: '+fecha.strftime("%w"))

#ejercicio 8
"""Escribe un programa en Python para convertir
una c a d e n a a datetime."""
from datetime import datetime

# Cadena de ejemplo que representa una fecha y hora
fecha_str = "Jan 1 2014 2:43PM"

fecha_datetime = datetime.strptime(fecha_str, "%b %d %Y %I:%M%p")

# Imprimir el resultado
print("Resultado:", fecha_datetime)


#ejercicio 9
"""Escribe un programa en Python para obtener la
hora actual."""
from datetime import datetime

# Obtenemos la fecha y hora actual
hora_actual = datetime.now()

print("Hora actual:", hora_actual.strftime("%H:%M:%S"))

#ejercicio 10
"""Escribe un programa en Python para restar cinco
días a la fecha actual."""

from datetime import datetime, timedelta

# Obtenemos la fecha actual
fecha_actual = datetime.now()

nueva_fecha = fecha_actual - timedelta(days=5)

print("Fecha hace 5 días:", nueva_fecha.strftime("%Y-%m-%d"))

#ejercicio 11
"""Escribe un programa en Python para convertir
una c a d e n a de marcas de tiempo unix en una
fecha legible."""
from datetime import datetime

timestamp = 1284105682

# Convertimos la marca de tiempo a una fecha legible
fecha_legible = datetime.fromtimestamp(timestamp)

print("Fecha legible:", fecha_legible.strftime("%Y-%m-%d %H:%M:%S"))

#ejercicio 12
"""Escribe un programa en Python para sumar 5
segundos con la hora actual"""
from datetime import datetime, timedelta

# Obtenemos la hora actual
hora_actual = datetime.now()

nueva_hora = hora_actual + timedelta(seconds=5)

# Imprimimos la hora actual y la nueva hora
print("Hora actual:", hora_actual.strftime("%Y-%m-%d %H:%M:%S"))
print("Hora después de 5 segundos:", nueva_hora.strftime("%Y-%m-%d %H:%M:%S"))

#ejercicio 13
"""Escribe un programa en Python para obtener el
n ú m e r o d e la s e m a n a ."""

import datetime

def semana(fecha=None):

    fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d')
    numero_semana = fecha.isocalendar()[1]
    return numero_semana

fecha = input("Ingrese una fecha en formato YYYY-MM-DD: ")
resultado = semana(fecha)
print("Número de la semana:", resultado)


#ejercicio 14
"""Escribe un programa en Python para seleccionar
todos los domingos de un año determinado."""
import datetime

def total_domingo(year):
    domingos = []
    fecha = datetime.date(year, 1, 1)
    while fecha.weekday() != 6:
        fecha += datetime.timedelta(days=1)

    while fecha.year == year:
        domingos.append(fecha)
        fecha += datetime.timedelta(days=7)

    return domingos

year = int(input("Introduce el año: "))
domingos = total_domingo(year)

print(f"Domingos del año {year}:")
for domingo in domingos:
    print(domingo)

#ejercicio 15
"""Escribe un programa en Python para contar el
número de lunes del primer día del mes desde
2015 h a s t a 2016."""

import datetime

def contar_lunes(inicio, fin):
    contador_lunes = 0

    for año in range(inicio, fin + 1):
        for mes in range(1, 13):
            primer_dia = datetime.date(año, mes, 1)

            if primer_dia.weekday() == 0:
                contador_lunes += 1

    return contador_lunes

inicio = 2015
fin = 2016

numero_lunes = contar_lunes(inicio, fin)


print(f"El número de lunes que cayeron en el primer día del mes desde {inicio} hasta {fin} es: {numero_lunes}")

#ejercicio 16
"""Escribe un programa en Python para crear 12
fechas fijas a partir de una fecha especificada en
un periodo determinado. La diferencia e n t r e dos
fechas será d e 20."""
import datetime

def nuevas_fechas(fecha_inicial, num_fechas, diferencia_dias):
    fechas = []

    fechas.append(fecha_inicial)

    for _ in range(1, num_fechas):

        nueva_fecha = fechas[-1] + datetime.timedelta(days=diferencia_dias)
        fechas.append(nueva_fecha)

    return fechas

año = int(input("Año de la fecha inicial (YYYY): "))
mes = int(input("Mes de la fecha inicial (MM): "))
dia = int(input("Día de la fecha inicial (DD): "))

fecha_inicial = datetime.date(año, mes, dia)

num_fechas = 12
diferencia_dias = 20

fechas = nuevas_fechas(fecha_inicial, num_fechas, diferencia_dias)

print("\nLas 12 fechas generadas con una diferencia de 20:")
for fecha in fechas:
    print(fecha)

#ejercicio 17
"""Implementa una función generadora que dadas
d o s listas del mismo tamaño, devuelva la
multiplicación e n t r e los e l e m e n t o s de c a d a una,
el primer elemento de la lista 1 por el primero de
la lista 2, el segundo con el segundo y así
sucesivamente. Sigue la siguiente estructura:"""

def multiplicar_listas(lista1, lista2):

    if len(lista1) != len(lista2):
        raise ValueError("Las listas deben tener el mismo tamaño.")

    for elemento1, elemento2 in zip(lista1, lista2):
        yield elemento1 * elemento2

lista1 = [1, 2, 3, 4, 5]
lista2 = [10, 20, 30, 40, 50]

resultado = multiplicar_listas(lista1, lista2)

while True:
    try:
        producto = next(resultado)
        print(producto)
    except StopIteration:
        print("Fin de la iteración, no hay más elementos.")
        break

#ejercicio 18
"""Implementa un generador, que dado un entero n,
genere n números aleatorios. Puedes usar el
método random d e la librería random para
generar n ú m e r o s aleatorios."""
import random

def generador_aleatorio(n):
    for _ in range(n):
        yield random.randint(1, 100)


n = int(input("Ingrese un número entero (n): "))

print(f"Generando números aleatorios:")
for numero in generador_aleatorio(n):
    print(numero)

#ejercicio 19
"""Implementa un generador de Fibonacci que
genere n números de la secuencia de Fibonacci,
que tiene la forma:
0, 1, 1, 2, 3, 5, 8, 13, ...
C u y o s d o s p r i m e r o s v a l o r e s s o n 0 y 1 p o r
definición y el resto s e calculan sumando los dos
ú l t i m o s v a l o r e s d e la s u c e s i ó n ."""
def generador_fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a  # Generamos el siguiente número de la secuencia
        a, b = b, a + b

n = int(input("Ingrese la cantidad de números de Fibonacci a generar: "))


print(f"Números de la secuencia de Fibonacci:")
for numero in generador_fibonacci(n):
    print(numero)

#ejercicio 20
"""Implementa un generador, que dado un entero n,
imprima todos los números inferiores a n
multiplicados por dos."""
def generar_multiplos(n):

  for i in range(2, n, 2):
    yield i


n = int(input("Ingrese Valor de N en entero"))

for numero in generar_multiplos(n):
  print(numero)

#ejercicio 21
"""Implementa un generador, que dado un entero n,
genere n número senares."""
def excepcion():
    try:
        raise ValueError("Este es un mensaje de error personalizado")
    except Exception as e:
        # Capturar el tipo de la excepción
        tipo_excepcion = type(e).__name__
        argumentos_excepcion = e.args
        mensaje_error = str(e)

        print(f"Tipo de excepción: {tipo_excepcion}")
        print(f"Argumentos de la excepción: {argumentos_excepcion}")
        print(f"Mensaje de error: {mensaje_error}")

excepcion()

#ejercicio 22
"""Crea una función que compute la diferencia
e n t r e d o s enteros. En c a s o d e q u e la diferencia
sea negativa genera una excepción inventada
por ti que informe sobre ello. Por ejemplo. la
excepción podría llamarse
NegativeDifferenceException."""

class NegativeDifferenceException(Exception):
    def __init__(self, message):
        super().__init__(message)


def diferencia(a, b):
    diferencia = a - b
    if diferencia < 0:
        raise NegativeDifferenceException(f"La diferencia es negativa: {diferencia}")
    return diferencia

try:
    resultado = diferencia(3, 5)
    print(f"La diferencia es: {resultado}")
except NegativeDifferenceException as e:
    print(f"Excepción capturada: {e}")

#ejercicio 23
"""Crea una función que calcule la división entre
dos números. Debe imprimir el mensaje 'Los
parámetros deben ser número enteros' cuando
se genera una excepción de tipo y 'El divisor no
puede ser 0' cuando se genera un
z e r o d i v i s i o n e r r o r."""

class NegativeDifferenceException(Exception):
    def __init__(self, message):
        super().__init__(message)


def diferencia(a, b):
    diferencia = a - b
    if diferencia < 0:
        raise NegativeDifferenceException(f"La diferencia es negativa: {diferencia}")
    return diferencia


def division(a, b):
    try:
        resultado = a / b
        return resultado
    except TypeError:
        print("Los parámetros deben ser número enteros")
    except ZeroDivisionError:
        print("El divisor no puede ser 0")

try:
    resultado = diferencia(3, 5)
    print(f"La diferencia es: {resultado}")
except NegativeDifferenceException as e:
    print(f"Excepción capturada: {e}")

resultado_division = division(10, 0)

#ejercicio 24
"""Añade a la función anterior, un mensaje que se
imprima al final de la ejecución de la función
independientemente de si se ha generado
excepción o no."""

class NegativeDifferenceException(Exception):
    def __init__(self, message):
        super().__init__(message)


def diferencia(a, b):
    diferencia = a - b
    if diferencia < 0:
        raise NegativeDifferenceException(f"La diferencia es negativa: {diferencia}")
    return diferencia


def division(a, b):
    try:
        resultado = a / b
        return resultado
    except TypeError:
        print("Los parámetros deben ser número enteros")
    except ZeroDivisionError:
        print("El divisor no puede ser 0")
    finally:
        print("Ejecución de la función calcular_division finalizada.")

try:
    resultado = diferencia(3, 5)
    print(f"La diferencia es: {resultado}")
except NegativeDifferenceException as e:
    print(f"Excepción capturada: {e}")

resultado_division = division(10, 0)
resultado_division = division(10, "a")
resultado_division = division(10, 2)