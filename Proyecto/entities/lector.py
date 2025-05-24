import os
import csv
import json
import pandas as pd
from typing import List, Dict, Any

class Lector:
    def __init__(self, path: str):
        self.path = path

    def _comprueba_extension(self, extension: str):
        """Comprueba si el archivo tiene la extensión correcta."""
        if not self.path.lower().endswith(extension.lower()):
            raise ValueError(f"El archivo no tiene la extensión {extension}")

    def lee_archivo(self):
        """Método base (debe ser implementado por las subclases)."""
        raise NotImplementedError("Este método debe ser implementado por las subclases")

    @staticmethod
    def convierte_dict_a_csv(data: Dict[str, Any]) -> pd.DataFrame:
        """Convierte un diccionario a un DataFrame."""
        return pd.DataFrame([data])

class LectorCSV(Lector):
    def __init__(self, path: str):
        super().__init__(path)
        self._comprueba_extension('.csv')

    def lee_archivo(self, datetime_columns: List[str] = None) -> pd.DataFrame:
        """Lee un archivo CSV y devuelve un DataFrame."""
        if datetime_columns is None:
            datetime_columns = []
        return pd.read_csv(self.path, parse_dates=datetime_columns)

class LectorJSON(Lector):
    def __init__(self, path: str):
        super().__init__(path)
        self._comprueba_extension('.json')

    def lee_archivo(self) -> List[Dict[str, Any]]:
        """Lee un archivo JSON y devuelve una lista de diccionarios."""
        with open(self.path, 'r', encoding='utf-8') as file:
            return json.load(file)

class LectorTXT(Lector):
    def __init__(self, path: str):
        super().__init__(path)
        self._comprueba_extension('.txt')

    def lee_archivo(self) -> List[Dict[str, Any]]:
        """Lee un archivo TXT y devuelve una lista de diccionarios."""
        data = []
        with open(self.path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    parts = line.strip().split(',')
                    data.append({
                        'id': parts[0],
                        'fecha_llegada': parts[1],
                        'retraso': parts[2],
                        'tipo_vuelo': parts[3],
                        'destino': parts[4]
                    })
        return data