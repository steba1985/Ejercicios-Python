import pandas as pd
from datetime import timedelta

class Slot:
    def __init__(self):
        self.id = None
        self.fecha_inicial = None
        self.fecha_final = None

    def asigna_vuelo(self, id, fecha_llegada, fecha_despegue):
        """Asigna un vuelo a este slot."""
        self.id = id
        self.fecha_inicial = fecha_llegada
        self.fecha_final = fecha_despegue

    def slot_esta_libre_fecha_determinada(self, fecha):
        """Verifica si el slot está libre en una fecha determinada."""
        if self.fecha_inicial is None:
            return timedelta(minutes=0)
        
        tiempo_restante = (self.fecha_final - fecha).total_seconds() / 60
        return max(timedelta(minutes=tiempo_restante), timedelta(minutes=0))