#ejercicio 1

import pandas as pd

df = pd.read_csv("Ejercicios Módulo 2 Temas 1 y 2/Modulo 5/Automobile_data.csv")
print(df.head())
print(df.tail())

#ejercicio 2

df.replace(["?", "n.a", "NaN"], pd.NA, inplace=True)
df.to_csv("Ejercicios Módulo 2 Temas 1 y 2/Modulo 5/limpio.csv", index=False)

#ejercicio 3
df = pd.read_csv("Ejercicios Módulo 2 Temas 1 y 2/Modulo 5/Automobile_data.csv")
caro = df.loc[df['price'].idxmax()]
print(f"Empresa: {caro['company']}, Precio: {caro['price']}")

#ejercicio 4
print(df[df['company'] == 'toyota'])

#ejercicio 5
print(df['company'].value_counts())

#ejercicio 6

coches_mas_caros = df.loc[df.groupby('company')['price'].idxmax()]

resultado = coches_mas_caros[['company', 'price']].sort_values(by='price', ascending=False)

print(resultado)

#ejercicio 7
kilometraje_medio = df.groupby('company')['average-mileage'].mean().reset_index()

kilometraje_medio = kilometraje_medio.sort_values(by='average-mileage', ascending=False)

print(kilometraje_medio)

#ejercicio 8
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df_ordenado_desc = df.sort_values(by='price', ascending=False)

print(df_ordenado_desc[['company', 'body-style', 'price']])

#ejercicio 9:
GermanCars = {'Company': ['Ford', 'Mercedes', 'BMV', 'Audi'], 
              'Price': [23845, 171995, 135925, 71400]}
japaneseCars = {'Company': ['Toyota', 'Honda', 'Nissan', 'Mitsubishi'], 
                'Price': [29995, 23600, 61500, 58900]}

df_german = pd.DataFrame(GermanCars)
df_japanese = pd.DataFrame(japaneseCars)
df_combined = pd.concat([df_german, df_japanese], ignore_index=True)

print(df_combined)

#ejercicio 10
Car_Price = {'Company': ['Toyota', 'Honda', 'BMV', 'Audi'], 
             'Price': [23845, 17995, 135925, 71400]}
car_Horsepower = {'Company': ['Toyota', 'Honda', 'BMV', 'Audi'], 
                  'horsepower': [141, 80, 182, 160]}

df_price = pd.DataFrame(Car_Price)
df_horsepower = pd.DataFrame(car_Horsepower)
df_combined = pd.merge(df_price, df_horsepower, on='Company')

print(df_combined)