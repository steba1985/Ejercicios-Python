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
                f"{super().ver()}")


profesor = Profesor(role="Docente", dept="Matemáticas", salary=45000, nombre="Juan Pérez", edad=40)
print(profesor.ver())

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