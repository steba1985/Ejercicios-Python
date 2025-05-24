import pandas as pd
from datetime import timedelta
from slot import Slot

class Aeropuerto:
    def __init__(self, vuelos: pd.DataFrame, slots: int, t_embarque_nat: int, t_embarque_internat: int):
        self.df_vuelos = vuelos
        self.n_slots = slots
        self.slots = {}
        self.tiempo_embarque_nat = t_embarque_nat
        self.tiempo_embarque_internat = t_embarque_internat

        for i in range(1, self.n_slots + 1):
            self.slots[i] = Slot()

        self.df_vuelos['fecha_despegue'] = pd.NaT
        self.df_vuelos['slot'] = 0

    def calcula_fecha_despegue(self, row) -> pd.Series:
        """Calcula la fecha de despegue basada en el tipo de vuelo."""
        if row['tipo_vuelo'] == 'NAT':
            fecha_despegue = row['fecha_llegada'] + timedelta(minutes=self.tiempo_embarque_nat)
        else:  # INTERNAT
            fecha_despegue = row['fecha_llegada'] + timedelta(minutes=self.tiempo_embarque_internat)
        
        row['fecha_despegue'] = fecha_despegue
        return row

    def encuentra_slot(self, fecha_vuelo) -> int:
        """Encuentra el primer slot disponible para una fecha dada."""
        for slot_id, slot in self.slots.items():
            if slot.slot_esta_libre_fecha_determinada(fecha_vuelo) == timedelta(minutes=0):
                return slot_id
        return -1

    def asigna_slot(self, vuelo) -> pd.Series:
        """Asigna un slot a un vuelo."""
        vuelo = self.calcula_fecha_despegue(vuelo)
        slot_id = self.encuentra_slot(vuelo['fecha_llegada'])
        
        if slot_id == -1:
            return vuelo
        
        self.slots[slot_id].asigna_vuelo(
            vuelo['id'],
            vuelo['fecha_llegada'],
            vuelo['fecha_despegue']
        )
        
        vuelo['slot'] = slot_id
        return vuelo

    def asigna_slots(self):
        """Asigna slots a todos los vuelos en el DataFrame."""
        self.df_vuelos = self.df_vuelos.apply(self.asigna_slot, axis=1)