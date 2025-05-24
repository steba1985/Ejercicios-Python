#ejercicio 1

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Ejercicios Módulo 2 Temas 1 y 2/Modulo 5/company_sales_data.csv")
plt.plot(df['month_number'], df['total_profit'])
plt.xlabel("Número de mes")
plt.ylabel("Beneficio total")
plt.show()

#ejercicio 2

plt.plot(df['month_number'], df['total_profit'], 
         linestyle='--', color='red', marker='o', linewidth=3, label='Beneficio')
plt.legend(loc='lower right')
plt.xlabel("Número de mes")
plt.ylabel("Unidades vendidas")
plt.show()

#ejercicio 3

productos = df.columns[1:6]  

plt.figure(figsize=(10, 6))

for producto in productos:
    plt.plot(df['month_number'], df[producto], marker='o', label=producto)

plt.title('Unidades vendidas por mes (por producto)')
plt.xlabel('Número de mes')
plt.ylabel('Unidades vendidas')
plt.xticks(df['month_number'])  
plt.grid(linestyle='--', alpha=0.7)
plt.legend(loc='upper left')  

plt.show()

#ejercicio 4

plt.figure(figsize=(10, 6))

plt.scatter(
    df['month_number'],  
    df['toothpaste'],    
    color='blue',        
    marker='o',          
    s=100,               
    label='Ventas de pasta de dientes'
)

plt.title('Ventas mensuales de pasta de dientes', fontsize=14)
plt.xlabel('Número de mes', fontsize=12)
plt.ylabel('Unidades vendidas', fontsize=12)
plt.xticks(df['month_number'])  
plt.grid(linestyle='-', linewidth=0.5, alpha=0.7)

plt.legend()
plt.show()

#ejercicio 5

plt.figure(figsize=(12, 6))
width = 0.35  
x = df['month_number']

plt.bar(
    x - width/2,          
    df['facecream'],      
    width=width,          
    label='Crema facial', 
    color='royalblue'     
)

plt.bar(
    x + width/2,          
    df['facewash'],       
    width=width,          
    label='Lavado de cara',
    color='lightcoral'
)

plt.title('Ventas mensuales: Crema facial vs Lavado de cara', fontsize=14)
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Unidades vendidas', fontsize=12)
plt.xticks(x)  
plt.grid(axis='y', linestyle='--', alpha=0.7)  
plt.legend()  

plt.show()

#ejercicio 6

plt.figure(figsize=(12, 6))

plt.bar(
    df['month_number'],  
    df['bathingsoap'],   
    color='teal',        
    width=0.6,           
    label='Jabón de baño'
)

plt.title('Ventas mensuales de jabón de baño', fontsize=14)
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Unidades vendidas', fontsize=12)
plt.xticks(df['month_number'])  
plt.grid(axis='y', linestyle='--', alpha=0.7)  
plt.legend()  

plt.savefig('ventas_jabon_barras.png', dpi=300, bbox_inches='tight')
plt.show()

#ejercicio 7

plt.figure(figsize=(10, 6))

plt.hist(
    df['total_profit'],  
    bins=5,              
    edgecolor='black',   
    color='orange',     
    alpha=0.5            
)

plt.title('Distribución de beneficios mensuales', fontsize=14)
plt.xlabel('Rango de beneficio (en dólares)', fontsize=12)
plt.ylabel('Frecuencia (número de meses)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.5)  
plt.show()

# ejercicio 8
productos = ['facecream', 'facewash', 'toothpaste', 'bathingsoap', 'shampoo', 'moisturizer']
ventas_totales = df[productos].sum()

plt.figure(figsize=(10, 8))

colores = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#C2C2F0', '#FFB3E6']

plt.pie(
    ventas_totales,
    labels=ventas_totales.index,
    autopct='%1.1f%%',       
    startangle=90,           
    shadow=True,             
    explode=[0.02]*len(ventas_totales), 
    colors=colores,
    wedgeprops={'edgecolor': 'white', 'linewidth': 1}  
)

plt.title('Distribución porcentual de ventas anuales por producto', fontsize=16, pad=20)
plt.tight_layout()
plt.show()

#ejercicio 9

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))  

ax1.plot(df['month_number'], df['bathingsoap'], 
         marker='o', 
         color='blue',
         linewidth=2,
         label='Ventas mensuales')
ax1.set_title('Tendencia anual de jabón de baño', fontsize=12)
ax1.set_xlabel('Mes', fontsize=10)
ax1.set_ylabel('Unidades vendidas', fontsize=10)
ax1.grid(linestyle='--', alpha=0.6)
ax1.legend()

ax2.plot(df['month_number'], df['facewash'], 
        marker='o', 
        color='skyblue',
        linewidth=2,
        label='Ventas Mensuales')
ax2.set_title('Tendencia anual del jabón de cara', fontsize=12)
ax2.set_xlabel('Mes', fontsize=10)
ax2.set_ylabel('Unidades vendidas', fontsize=10)
ax2.grid(linestyle='--', alpha=0.6)
ax2.legend()

plt.suptitle('Análisis de ventas', fontsize=14, y=1.02)
plt.tight_layout()
plt.show()

#ejercicio 10

productos = ['facecream', 'facewash', 'toothpaste', 'bathingsoap', 'shampoo', 'moisturizer']
meses = df['month_number']
ventas = df[productos]

plt.figure(figsize=(12, 7))

colores = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#C2C2F0', '#FFB3E6']
plt.stackplot(
    meses,
    ventas.T,  
    labels=productos,
    colors=colores,
    edgecolor='white',
    linewidth=0.5
)

plt.title('Ventas acumuladas por producto (año completo)', fontsize=16, pad=20)
plt.xlabel('Mes', fontsize=12)
plt.ylabel('Unidades vendidas', fontsize=12)
plt.xticks(meses)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))  

plt.tight_layout()
plt.show()