"""Proyecto: Gestión de un Centro Médico
Descripción:
Crearás una aplicación de consola que permita al usuario gestionar pacientes y citas en un centro médico. 
Cada paciente tendrá un nombre, edad y número de identificación, y cada cita tendrá un paciente asociado, 
un médico, una fecha y una hora.

Funcionalidades:
Registrar un nuevo paciente.
Programar una nueva cita.
Ver todos los pacientes.
Ver todas las citas.
Cancelar una cita.
Salir de la aplicación.

Estructura del Proyecto:
Clase Paciente: Representa un paciente individual.
Clase Cita: Representa una cita médica.
Clase CentroMedico: Gestiona pacientes y citas.
Funciones auxiliares: Mostrar menú y procesar la selección del usuario."""


class medico:
    def __init__(self,nombre,especialidad):
        self.nombre=nombre
        self.especialidad=especialidad

class paciente:
    def __init__(self,nie,nombre,edad):
        self.nie=nie
        self.nombre=nombre
        self.edad=edad

class cita:
    def __init__(self,fecha):
        self.fecha=fecha
    
    def gen_cita(fecha,paciente,medico):
        

    
