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

# Agrupación de datos por protocolo y minuto, y sumando los paquetes
grouped_data = data.groupby(['Proto', 'Minute seen'])['In Pkt'].sum().reset_index()

# Agrupación de datos por minuto para todos los protocolos y sumando los paquetes
total_data = data.groupby('Minute seen')['In Pkt'].sum().reset_index()

# Creación de un gráfico para cada protocolo
for protocol in grouped_data['Proto'].unique():
    protocol_data = grouped_data[grouped_data['Proto'] == protocol]
    plt.plot(protocol_data['Minute seen'], protocol_data['In Pkt'], label=protocol)

# Creación de un gráfico para el total
plt.plot(total_data['Minute seen'], total_data['In Pkt'], label='Total', linestyle='--')

# Configuración del gráfico
plt.xlabel('Tiempo')
plt.ylabel('Número de paquetes (Escala Log)')
plt.title('Número de paquetes por minuto para cada protocolo')
plt.legend(title='Protocolo')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.yscale('log')  # escala logarítmica para el eje y
plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=2))  # escala de 2 minutos
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))  # formato de la hora en HH:MM
plt.show()
