import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Lectura del CSV
data = pd.read_csv('salida_ordenada.csv', delimiter=',')
data.columns = ["Date first seen", "Date last seen", "Proto", "Src IP Addr", "Dst IP Addr", "Src Pt", "Dst Pt", "In Pkt", "In Byte"]

# Limpiar el DataFrame
data = data[data['Date first seen'].str.contains('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{3}', na=False)]
data['Date first seen'] = pd.to_datetime(data['Date first seen'], format='%Y-%m-%d %H:%M:%S.%f')

# Creación de una nueva columna para el minuto en el que se vio por primera vez
data['Minute seen'] = data['Date first seen'].dt.floor('min')

# Agrupación de datos por puerto y minuto, y sumando los paquetes
grouped_data = data.groupby(['Dst Pt', 'Minute seen'])['In Pkt'].sum().reset_index()

# Ajustar el tamaño del gráfico
plt.figure(figsize=(12, 7))

# Creación de un gráfico para cada puerto
for port in grouped_data['Dst Pt'].unique():
    port_data = grouped_data[grouped_data['Dst Pt'] == port]
    plt.plot(port_data['Minute seen'], port_data['In Pkt'], label=f'Puerto {port}')

# Configuración del gráfico
plt.xlabel('Tiempo')
plt.ylabel('Número de paquetes (Escala Log)')
plt.title('Número de paquetes por minuto para cada puerto de destino')
plt.legend(title='Puerto de Destino', loc='upper left', bbox_to_anchor=(0.98, 1))  # Ajuste de la posición de la leyenda
plt.xticks(rotation=45)
plt.grid(True)
plt.yscale('log')  # escala logarítmica para el eje y
plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=2))  # escala de 2 minutos
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # formato de la hora en HH:MM

plt.show()

