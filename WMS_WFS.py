import tkinter as tk
from tkinter import ttk
from tkinter import ttk, filedialog, messagebox
from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
import pandas as pd
import folium
import requests
import os

def get_wms_layers(wms_url, output_path):
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
        
        # Crear DataFrame de Pandas
        df = pd.DataFrame(layers_info)
        # Exportar el DataFrame a un archivo CSV en la ruta de salida definida
        df.to_csv(output_path, index=False, sep=',')
        print("El archivo CSV ha sido exportado correctamente en:", output_path)
        status_label.config(text="El CSV fue generado correctamente.", foreground="green")
        return df
    except Exception as e:
        print("Error:", e)
        status_label.config(text="Proporcione un servicio WMS.", foreground="red")
        return None
    
def select_output_directory_wfs():
    output_directory = filedialog.askdirectory()
    if output_directory:
        wfs_output_directory_entry.delete(0, tk.END)
        wfs_output_directory_entry.insert(0, output_directory)

def mostrar_mapa():
    wms_url = wms_url_entry.get()
    if '/wms' not in wms_url.lower():
        print("La URL ingresada no parece ser para un servicio WMS. Por favor, proporcione una URL de un servicio WMS.")
        status_label.config(text="Proporcione un servicio WMS.", foreground="red")
        return
    
    try:
        layers_df = get_wms_layers(wms_url, "temp_wms_layers.csv")
        if layers_df is not None:
            m = folium.Map(location=[0, 0], zoom_start=2)
            for index, row in layers_df.iterrows():
                layer = folium.raster_layers.WmsTileLayer(
                    url=wms_url,
                    layers=row['Nombre'],
                    name=row['Título'],
                    fmt='image/png',
                    transparent=True,
                    show=False
                )
                layer.add_to(m)
            
            # Crear un control de capas para cada capa
            for index, row in layers_df.iterrows():
                folium.LayerControl(collapsed=False).add_to(m)
            
            m.save("mapa_interactivo.html")
            import webbrowser
            webbrowser.open("mapa_interactivo.html")
    except Exception as e:
        print("Error:", e)
        status_label.config(text="Error al mostrar el mapa.", foreground="red")

def get_wfs_layers(wfs_url, output_path):
    try:
        wfs = WebFeatureService(wfs_url)
        inicio_url = wfs_url[:wfs_url.find("/wfs")]
        layers_info = []
        for layer_name in wfs.contents:
            # Obtener el esquema de la capa actual
            describe_feature_type = wfs.get_schema(layer_name)
            attributes = list(describe_feature_type['properties'].keys())

            layer_info = {
                'Nombre': layer_name,
                'Título': wfs[layer_name].title,
                'Resumen': wfs[layer_name].abstract,
                'Atributos': attributes,  # Lista de nombres de atributos de la capa actual
                'URL_SHP': f"{inicio_url}/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName={layer_name}&outputFormat=SHAPE-ZIP"
            }
            layers_info.append(layer_info)
        
        # Crear DataFrame de Pandas
        df = pd.DataFrame(layers_info)
        # Exportar el DataFrame a un archivo CSV en la ruta de salida definida
        df.to_csv(output_path, index=False, sep=',')
        print("El archivo CSV ha sido exportado correctamente en:", output_path)
        status_label.config(text="El CSV fue generado correctamente.", foreground="green")
        return df
    except Exception as e:
        print("Error:", e)
        status_label.config(text="Proporcione un servicio WFS.", foreground="red")
        return None
    
def submit_wms():
    wms_url = wms_url_entry.get()
    output_path = output_directory_entry.get()
    
    if '/wms' not in wms_url.lower():
        print("La URL ingresada no parece ser para un servicio WMS. Por favor, proporcione una URL de un servicio WMS.")
        status_label.config(text="Proporcione un servicio WMS.", foreground="red")
        return
    
    get_wms_layers(wms_url, output_path)

def submit_wfs():
    wfs_url = wfs_url_entry.get()
    output_path = wfs_output_directory_entry.get()
    
    if '/wfs' not in wfs_url.lower():
        print("La URL ingresada no parece ser para un servicio WFS. Por favor, proporcione una URL de un servicio WFS.")
        status_label.config(text="Proporcione un servicio WFS.", foreground="red")
        return
    
    get_wfs_layers(wfs_url, output_path)

def select_output_directory():
    output_path = filedialog.asksaveasfilename(initialdir="/", title="Guardar CSV", filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")))
    if output_path:
        output_directory_entry.delete(0, tk.END)
        output_directory_entry.insert(0, output_path)

def select_wfs_output_directory():
    output_path = filedialog.asksaveasfilename(initialdir="/", title="Guardar CSV", filetypes=(("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")))
    if output_path:
        wfs_output_directory_entry.delete(0, tk.END)
        wfs_output_directory_entry.insert(0, output_path)

def download_wfs_layers(wfs_url, output_directory, progress_bar):
    try:
        wfs = WebFeatureService(wfs_url)
        inicio_url = wfs_url[:wfs_url.find("/wfs")]
        total_layers = len(wfs.contents)
        layers_downloaded = 0

        for layer_name in wfs.contents:
            layer_name_cleaned = layer_name.replace(':', '_')
            
            response = requests.get(f"{inicio_url}/wfs?service=WFS&version=1.0.0&request=GetFeature&typeName={layer_name}&outputFormat=application/json")
            if response.status_code == 200:
                with open(f"{output_directory}/{layer_name_cleaned}.geojson", 'wb') as f:
                    f.write(response.content)
                print(f"Capa {layer_name} descargada exitosamente.")
                layers_downloaded += 1
                progress = (layers_downloaded / total_layers) * 100
                progress_bar['value'] = progress
                root.update_idletasks()  # Actualizar la interfaz gráfica
            else:
                print(f"No se pudo descargar la capa {layer_name}. Estado de la respuesta: {response.status_code}")

        print("Descarga de capas completada.")
        status_label.config(text="Descarga de capas completada.", foreground="green")
    except Exception as e:
        print("Error:", e)
        status_label.config(text="Error al descargar las capas.", foreground="red")

def download_wfs_layers_wrapper():
    wfs_url = wfs_url_entry.get()
    output_directory = wfs_output_directory_entry.get()

    if '/wfs' not in wfs_url.lower():
        print("La URL ingresada no parece ser para un servicio WFS. Por favor, proporcione una URL de un servicio WFS.")
        status_label.config(text="Proporcione un servicio WFS.", foreground="red")
        return

    if not os.path.exists(output_directory):
        print("El directorio de salida especificado no existe.")
        status_label.config(text="El directorio de salida especificado no existe.", foreground="red")
        return

    progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")
    progress_bar.pack(fill="x", padx=10, pady=10)

    download_wfs_layers(wfs_url, output_directory, progress_bar)
    progress_bar.destroy()  # Eliminar la barra de progreso cuando se completa la descarga

root = tk.Tk()
root.title("Aplicación WMS/WFS")

# Crear pestañas
tab_control = ttk.Notebook(root)
wms_tab = ttk.Frame(tab_control)
wfs_tab = ttk.Frame(tab_control)
tab_control.add(wms_tab, text='WMS')
tab_control.add(wfs_tab, text='WFS')
tab_control.pack(expand=1, fill="both")

# Crear widgets para la pestaña WMS
wms_url_label = ttk.Label(wms_tab, text="URL del servicio WMS:")
wms_url_label.pack(pady=(10, 0))
wms_url_entry = ttk.Entry(wms_tab, width=50)
wms_url_entry.pack(pady=(0, 10))

output_directory_label = ttk.Label(wms_tab, text="Definir ruta y nombre del archivo CSV:")
output_directory_label.pack(pady=(0, 0))
output_directory_entry = ttk.Entry(wms_tab, width=50)
output_directory_entry.pack(pady=(0, 10))
output_directory_button = ttk.Button(wms_tab, text="Seleccionar archivo de salida", command=select_output_directory)
output_directory_button.pack()

submit_button = ttk.Button(wms_tab, text="Generar CSV", command=submit_wms)
submit_button.pack(pady=(10, 0))

visualize_button = ttk.Button(wms_tab, text="Visualizar", command=mostrar_mapa)
visualize_button.pack(pady=(10, 0))

# Crear widgets para la pestaña WFS
wfs_url_label = ttk.Label(wfs_tab, text="URL del servicio WFS:")
wfs_url_label.pack(pady=(10, 0))
wfs_url_entry = ttk.Entry(wfs_tab, width=50)
wfs_url_entry.pack(pady=(0, 10))

wfs_output_directory_label = ttk.Label(wfs_tab, text="Definir ruta y nombre del archivo:")
wfs_output_directory_label.pack(pady=(0, 0))
wfs_output_directory_entry = ttk.Entry(wfs_tab, width=50)
wfs_output_directory_entry.pack(pady=(0, 10))
wfs_output_directory_button = ttk.Button(wfs_tab, text="Seleccionar archivo de salida", command=select_wfs_output_directory)
wfs_output_directory_button.pack(side="top", pady=5)

wfs_submit_button = ttk.Button(wfs_tab, text="Generar CSV", command=submit_wfs)
wfs_submit_button.pack(side="top", pady=5)

status_label = ttk.Label(root, text="")
status_label.pack(pady=(10, 0))

# Botón para seleccionar el directorio de salida
wfs_output_directory_button = ttk.Button(wfs_tab, text="Seleccionar directorio de salida", command=select_output_directory_wfs)
wfs_output_directory_button.pack(side="top", pady=(10, 0))

# Botón "Descargar"
download_button = ttk.Button(wfs_tab, text="Descargar", command=download_wfs_layers_wrapper)
download_button.pack(side="top", pady=5)

status_label = ttk.Label(root, text="")
status_label.pack(pady=(10, 0))

# Pestaña de Autoría
tab_autoria = ttk.Frame(tab_control)
tab_control.add(tab_autoria, text='Autoría')

# Contenido de la pestaña de Autoría
frame_autor = ttk.Frame(tab_autoria)
frame_autor.pack(pady=10)

label_autor = ttk.Label(frame_autor, text="APLICACIÓN WMS/ WFS")
label_autor.pack()
label_autor = ttk.Label(frame_autor, text="Versión 1 en desarrollo")
label_autor.pack()
label_autor = ttk.Label(frame_autor, text="Autor: Ing. Agrim. Matías Pose")
label_autor.pack()
label_contacto = ttk.Label(frame_autor, text="Repositorio: https://github.com/pmatiasn/aplicacion_wms_wfs")
label_contacto.pack()

root.mainloop()