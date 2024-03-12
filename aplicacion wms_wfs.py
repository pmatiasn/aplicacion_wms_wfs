#pip install owslib geopandas
#pip install folium


import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from owslib.wfs import WebFeatureService
from owslib.wms import WebMapService
import pandas as pd
import folium
import webbrowser

def get_wms_layers(wms_url):
    try:
        wms = WebMapService(wms_url)
        layers_info = []
        for layer_name in wms.contents:
            layer_info = {
                'Nombre': layer_name,
                'Título': wms[layer_name].title,
                'Resumen': wms[layer_name].abstract
            }
            layers_info.append(layer_info)
        return layers_info
    except Exception as e:
        print("Error:", e)
        return None

def get_wfs_layers(wfs_url):
    try:
        wfs = WebFeatureService(wfs_url)
        inicio_url = wfs_url[:wfs_url.find("/wf")]
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

def browse_file():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    entry_path.delete(0, tk.END)
    entry_path.insert(0, filename)

def run_code():
    url = entry_url.get()
    path = entry_path.get()

    if "wms" in url.lower() and var.get() != 1:
        message_label.config(text="Ha seleccionado WMS pero está usando una URL de WFS.")
        return
    elif "wfs" in url.lower() and var.get() != 2:
        message_label.config(text="Ha seleccionado WFS pero está usando una URL de WMS.")
        return

    message_label.config(text="Ejecutando el código...")

    if var.get() == 1:
        layers_info = get_wms_layers(url)
        filename = f"{path}.csv"
    elif var.get() == 2:
        layers_info = get_wfs_layers(url)
        filename = f"{path}.csv"
    else:
        message_label.config(text="Seleccione una opción válida (WMS o WFS)")
        return

    if layers_info:
        df = pd.DataFrame(layers_info)
        df.to_csv(filename, index=False, sep=',')
        message_label.config(text="El archivo CSV ha sido exportado correctamente.")
        print(df.to_string(index=False))
    else:
        message_label.config(text="No se pudieron recuperar las capas.")

def mostrar_mapa():
    wms_url = url_entry_visualizar.get()

    if not wms_url.lower().startswith('http'):
        message_label_visualizar.config(text="La URL ingresada no parece ser válida.")
        return

    if "wms" not in wms_url.lower():
        message_label_visualizar.config(text="Por favor, ingrese una URL de servicio WMS.")
        return

    layers_info = get_wms_layers(wms_url)
    if layers_info:
        m = folium.Map(location=[0, 0], zoom_start=2, control_scale=True)

        # Agregar capa de imágenes satelitales (Google Satellite)
        satellite_layer = folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', name='Google Satellite', attr='Google')
        m.add_child(satellite_layer)

        folium.TileLayer('openstreetmap').add_to(m)
        for layer_info in layers_info:
            layer_name = layer_info['Nombre']
            layer_title = layer_info['Título']
            layer = folium.raster_layers.WmsTileLayer(
                url=wms_url,
                name=layer_title,
                fmt='image/png',
                layers=layer_name,
                transparent=True,
                overlay=True,
                show=False
            )
            layer.add_to(m)
        folium.LayerControl(collapsed=False).add_to(m)
        m.save('mapa.html')
        webbrowser.open('mapa.html')
    else:
        print("No se pudieron recuperar las capas.")

# Crear ventana principal
root = tk.Tk()
root.title("Aplicación WMS/WFS")

# Crear control de pestañas
tab_control = ttk.Notebook(root)

# Pestaña de Consultas
tab_consultas = ttk.Frame(tab_control)
tab_control.add(tab_consultas, text='Consultas')

# Crear frames para la pestaña de Consultas
frame_options = ttk.Frame(tab_consultas)
frame_options.pack(pady=10)
frame_url = ttk.Frame(tab_consultas)
frame_url.pack(pady=10)
frame_path = ttk.Frame(tab_consultas)
frame_path.pack(pady=10)
frame_buttons = ttk.Frame(tab_consultas)
frame_buttons.pack(pady=10)
frame_message = ttk.Frame(tab_consultas)
frame_message.pack(pady=10)

# Opciones: WMS / WFS
var = tk.IntVar()
radio_wms = ttk.Radiobutton(frame_options, text="WMS", variable=var, value=1)
radio_wfs = ttk.Radiobutton(frame_options, text="WFS", variable=var, value=2)
radio_wms.grid(row=0, column=0, padx=5)
radio_wfs.grid(row=0, column=1, padx=5)

# URL
label_url = ttk.Label(frame_url, text="URL del servicio:")
label_url.grid(row=0, column=0, padx=5)
entry_url = ttk.Entry(frame_url, width=50)
entry_url.grid(row=0, column=1, padx=5)

# Directorio de salida
label_path = ttk.Label(frame_path, text="Archivo de salida:")
label_path.grid(row=0, column=0, padx=5)
entry_path = ttk.Entry(frame_path, width=50)
entry_path.grid(row=0, column=1, padx=5)
button_path = ttk.Button(frame_path, text="Seleccionar archivo", command=browse_file)
button_path.grid(row=0, column=2, padx=5)

# Botón para ejecutar el código
button_run = ttk.Button(frame_buttons, text="Ejecutar", command=run_code)
button_run.pack()

# Etiqueta para mensajes
message_label = ttk.Label(frame_message, text="")
message_label.pack()

# Pestaña de Visualizar
tab_visualizar = ttk.Frame(tab_control)
tab_control.add(tab_visualizar, text='Visualizar')

# Crear frames para la pestaña de Visualizar
frame_url_visualizar = ttk.Frame(tab_visualizar)
frame_url_visualizar.pack(pady=10)
frame_buttons_visualizar = ttk.Frame(tab_visualizar)
frame_buttons_visualizar.pack(pady=10)
frame_message_visualizar = ttk.Frame(tab_visualizar)
frame_message_visualizar.pack(pady=10)

# URL para visualizar
label_url_visualizar = ttk.Label(frame_url_visualizar, text="URL del servicio WMS:")
label_url_visualizar.grid(row=0, column=0, padx=5, pady=5, sticky="w")
url_entry_visualizar = ttk.Entry(frame_url_visualizar, width=50)
url_entry_visualizar.grid(row=0, column=1, padx=5, pady=5)

# Botón para mostrar el mapa
mostrar_mapa_button = ttk.Button(frame_buttons_visualizar, text="Mostrar Mapa", command=mostrar_mapa)
mostrar_mapa_button.pack()

# Etiqueta para mensajes en la pestaña de Visualizar
message_label_visualizar = ttk.Label(frame_message_visualizar, text="")
message_label_visualizar.pack()

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

# Añadir el control de pestañas a la ventana principal
tab_control.pack(expand=1, fill="both")

# Ejecutar el bucle principal de la ventana
root.mainloop()
