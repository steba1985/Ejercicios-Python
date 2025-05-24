import os
import pandas as pd
from entities.lector import LectorTXT, LectorCSV, LectorJSON
from entities.aeropuerto import Aeropuerto


def preprocess_data(df_list):
    """
    Preprocesa y combina los DataFrames de vuelos
    :param df_list: Lista de DataFrames con datos de vuelos
    :return: DataFrame único con todos los vuelos procesados
    """
    # Combinar todos los DataFrames
    combined_df = pd.concat(df_list, ignore_index=True)
    
    # Procesar retrasos (convertir '-' a 0 minutos)
    combined_df['retraso'] = combined_df['retraso'].apply(
        lambda x: pd.Timedelta(minutes=0) if x == '-' else pd.Timedelta(x))
    
    # Aplicar retrasos a las fechas de llegada
    combined_df['fecha_llegada'] += combined_df['retraso']
    
    # Ordenar por fecha de llegada
    combined_df.sort_values('fecha_llegada', inplace=True)
    
    return combined_df


if __name__ == '__main__':
    # Configuración inicial
    NUM_SLOTS = 3
    TIEMPO_EMBARQUE_NAT = 60  # minutos
    TIEMPO_EMBARQUE_INTERNAT = 100  # minutos
    
    # Rutas a los archivos de datos
    path_1 = os.path.abspath('./data/vuelos_1.txt')
    path_2 = os.path.abspath('./data/vuelos_2.csv')
    path_3 = os.path.abspath('./data/vuelos_3.json')
    
    try:
        # Leer y procesar los archivos de vuelos
        print("Leyendo archivos de vuelos...")
        
        # Crear lectores para cada tipo de archivo
        lector_txt = LectorTXT(path_1)
        lector_csv = LectorCSV(path_2)
        lector_json = LectorJSON(path_3)
        
        # Leer los datos
        datos_txt = lector_txt.lee_archivo()
        datos_csv = lector_csv.lee_archivo(datetime_columns=['fecha_llegada'])
        datos_json = lector_json.lee_archivo()
        
        # Convertir todos a DataFrames
        df_txt = pd.DataFrame(datos_txt)
        df_csv = pd.DataFrame(datos_csv)
        df_json = pd.DataFrame(datos_json)
        
        # Convertir fechas en los DataFrames que lo necesiten
        df_txt['fecha_llegada'] = pd.to_datetime(df_txt['fecha_llegada'])
        df_json['fecha_llegada'] = pd.to_datetime(df_json['fecha_llegada'])
        
        # Preprocesar y combinar los datos
        print("Procesando datos de vuelos...")
        vuelos_combinados = preprocess_data([df_txt, df_csv, df_json])
        
        # Crear instancia del aeropuerto
        print("Inicializando sistema de aeropuerto...")
        aeropuerto = Aeropuerto(
            vuelos=vuelos_combinados,
            slots=NUM_SLOTS,
            t_embarque_nat=TIEMPO_EMBARQUE_NAT,
            t_embarque_internat=TIEMPO_EMBARQUE_INTERNAT
        )
        
        # Asignar slots a los vuelos
        print("Asignando slots a los vuelos...")
        aeropuerto.asigna_slots()
        
        # Mostrar resultados
        print("\nResultado de la asignación de slots:")
        print(aeropuerto.df_vuelos[['id', 'fecha_llegada', 'fecha_despegue', 'slot', 'tipo_vuelo', 'destino']])
        
        # Guardar resultados en un archivo CSV
        output_path = os.path.abspath('./data/vuelos_asignados.csv')
        aeropuerto.df_vuelos.to_csv(output_path, index=False)
        print(f"\nResultados guardados en: {output_path}")
        
    except FileNotFoundError as e:
        print(f"Error: Archivo no encontrado - {e}")
    except ValueError as e:
        print(f"Error en los datos: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")