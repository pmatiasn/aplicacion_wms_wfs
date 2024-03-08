# pip install owslib geopandas

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from owslib.wfs import WebFeatureService
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
    
    # Verificar si la URL contiene "wms" o "wfs" para determinar el tipo de servicio
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

# Crear ventana principal
root = tk.Tk()
root.title("Capas dentro del WMS/WFS")

# Crear frames
frame_options = ttk.Frame(root)
frame_options.pack(pady=10)
frame_url = ttk.Frame(root)
frame_url.pack(pady=10)
frame_path = ttk.Frame(root)
frame_path.pack(pady=10)
frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=10)
frame_message = ttk.Frame(root)
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

root.mainloop()
