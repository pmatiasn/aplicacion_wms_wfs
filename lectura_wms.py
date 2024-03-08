# pip install owslib geopandas

from owslib.wms import WebMapService
import pandas as pd

def get_wms_layers(wms_url):
    try:
        wms = WebMapService(wms_url)
        layers_info = []
        for layer_name in wms.contents:
            layer = wms[layer_name]
            layer_info = {
                'Nombre': layer_name,
                'Título': layer.title,
                'Resumen': layer.abstract,
            }
            layers_info.append(layer_info)
        return layers_info
    except Exception as e:
        print("Error:", e)
        return None

# URL del servicio WMS
wms_url = input("Ingrese la URL del servicio WMS: ")

# Obtener información detallada de las capas
layers_info = get_wms_layers(wms_url)
if layers_info:
    # Crear un DataFrame de Pandas a partir de los datos de las capas
    df = pd.DataFrame(layers_info)
    # Exportar el DataFrame a un archivo CSV
    df.to_csv('capas_wms.csv', index=False, sep=',')
    print("El archivo CSV ha sido exportado correctamente.")
    # Mostrar el DataFrame
    print(df.to_string(index=False))
else:
    print("No se pudieron recuperar las capas.")