#ejercicio 1

class Jet:
    def __init__(self, name, country):
        self.name=name
        self.origin=country

first_item=Jet("F16","USA")

print ("Primer Atributo:{}".format(first_item.name))


#ejercicio 2

russia=Jet("SU33","Russia")
sweden=Jet("AJS37","Sweden")
france=Jet("Mirage2000","France")
usa=Jet("F14","USA")
ussr=Jet("Mig29","USSR")
usa1=Jet("A10","USA")


#ejercicio 3


class Jet1:
    def __init__(self, name, country, cantidad):
        self.name=name
        self.origin=country
        self.cant=cantidad

france=Jet1("Mirage2000","France",87)
usa=Jet1("F14","USA",35)

#ejercicio 4

class Nobel:
    def __init__(self,category,year,winner):
        self.category=category
        self.year=year
        self.winner=winner

np2005 = Nobel ("Peace", 2005, "Muhammad Yunus") 
print(np2005. category, np2005.year, np2005. winner)

#ejercicio 5

class Estudiante:
    def __init__(self, nombre, edad, grado):
        self.nombre=nombre
        self.edad=edad
        self.grado=grado

std = Estudiante("Alfredo","6","Primero")

print("Hola {} tu edad es {} y estudias {} grado".format(std.nombre, std.edad, std.grado))

#ejercicio 6

class Estudiante1:
    def __init__(self):
        pass


#ejercicio 7

class Estudiante2:
    def __init__(self, nombre, edad, grado):
        self.nombre=nombre
        self.edad=edad
        self.grado=grado      
    def calula_nota(self,lista): 
        suma=0
        for nota in lista:
            suma=suma+nota
        total=suma/len(lista)
        if total >= 5:
            self.grado="Avanza de Grado"
            print ("Felicitaciones {} tu nota final es: {} por lo tanto {}".format(self.nombre,total,self.grado))
        else:
            self.grado="No Avanza de Grado"
            print ("Lo Siento {} tu nota final es: {} por lo tanto {}".format(self.nombre,total,self.grado))
    @staticmethod
    def aprueba(nota):
        for x,y in nota:
            if nota[y]<5:
                print("La Asignatura {} tiene un puntaje de: {}".format(nota[x], nota[y]))
        
notas=[4,5,8,7]     
pru=Estudiante2("jose",10,"Quinto")
pru.calula_nota(notas)

#ejercicio 8

class Estudiante3:
    def __init__(self, nombre, edad, grado):
        self.nombre=nombre
        self.edad=edad
        self.grado=grado      
    def calula_nota(self,lista): 
        for nota in lista:
            suma=suma+nota
        total=suma/len(lista)
        if total >= 5:
            self.grado="Avanza de Grado"
            print ("Felicitaciones {} tu nota final es: {} por lo tanto {}".format(self.nombre,total,self.grado))
        else:
            self.grado="No Avanza de Grado"
            print ("Lo Siento {} tu nota final es: {} por lo tanto {}".format(self.nombre,total,self.grado))

    @staticmethod
    def aprueba(nota):
        for x in nota:
            if nota[x]<5:
                print("La Asignatura {} tiene un puntaje de: {}".format(x, nota[x]))

pru1=Estudiante3("jose",10,"Quinto")
asig={"Ingles":6,"Frances":4,"Física":6,"Historía":3}
Estudiante3.aprueba(asig)

#ejercicio 9

class Estudiante4:
    escuela='Victoria'
    def __init__(self, nombre, edad, grado):
        self.nombre=nombre
        self.edad=edad
        self.grado=grado   

    def calula_nota(self,lista): 
        for nota in lista:
            suma=suma+nota
        total=suma/len(lista)
        if total >= 5:
            self.grado="Avanza de Grado"
            print ("Felicitaciones {} tu nota final es: {} por lo tanto {}".format(self.nombre,total,self.grado))
        else:
            self.grado="No Avanza de Grado"
            print ("Lo Siento {} tu nota final es: {} por lo tanto {}".format(self.nombre,total,self.grado))

    @staticmethod
    def aprueba(nota):
        for x in nota:
            if nota[x]<5:
                print("La Asignatura {} tiene un puntaje de: {}".format(x, nota[x]))
    
    @classmethod
    def up_escuela(cls,escuela_new):
        cls.escuela=escuela_new
        return cls.escuela
    

pru1=Estudiante4("jose",10,"Quinto")
Estudiante4.up_escuela("Litin")
print("Nuevo Nombre de Escuela: {}".format(Estudiante4.escuela))     

#ejercicio 10

class Estudiante5:
    def __init__(self, nombre, edad, grado):
        self.nombre=nombre
        self.edad=edad
        self.grado=grado  

    def __asis(self,asist): 
        valor=0
        for x in asist:
            if asist[x]<4:
                valor=1
                break
        if valor==1:
            return valor
        else:
            for x in asist:
                if asist[x]>=4 and asist[x]<=8:
                    valor=2
                    break
            if valor==2:
                return valor
            else: 
                return 3
            

    def resultado(self,asistencia):
        self.asistencia=asistencia
        print("Resultado de Asistencia {}".format(self.__asis(asistencia)))
        

pru1=Estudiante5("jose",10,"Quinto")
asistencia={"Enero":13,"Febrero":9,"Marzo":11,"Abril":10}
pru1.resultado(asistencia)
