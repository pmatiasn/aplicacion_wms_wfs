# pip install owslib geopandas

from owslib.wfs import WebFeatureService
import pandas as pd

def get_wfs_layers(wfs_url):
    try:
        wfs = WebFeatureService(wfs_url)
        inicio_url= wfs_url[:wfs_url.find("/wf")]
        layers_info = []
        for layer_name in wfs.contents:
            layer_info = {
                'Nombre': layer_name,
                'Título': wfs[layer_name].title,
                'Resumen': wfs[layer_name].abstract,
                'URL_SHP': f"{inicio_url}/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName={layer_name}&outputFormat=SHAPE-ZIP",
            }
            layers_info.append(layer_info)
        return layers_info
    except Exception as e:
        print("Error:", e)
        return None

# URL del servicio WFS
wfs_url = input("Ingrese la URL del servicio WFS: ")

# Obtener información detallada de las capas
layers_info = get_wfs_layers(wfs_url)
if layers_info:
    # Crear un DataFrame de Pandas a partir de los datos de las capas
    df = pd.DataFrame(layers_info)
    # Exportar el DataFrame a un archivo CSV
    df.to_csv('capas_wfs.csv', index=False, sep=',')
    print("El archivo CSV ha sido exportado correctamente.")
    # Mostrar el DataFrame
    print(df.to_string(index=False))
else:
    print("No se pudieron recuperar las capas.")