# Aplicación WMS / WFS

Aplicación desarrollada en Python para la exploración, visualización y descarga de información geoespacial publicada mediante servicios OGC WMS (Web Map Service) y WFS (Web Feature Service).
Permite conectarse a servidores geográficos, inspeccionar sus capas, generar informes técnicos, visualizar información sobre mapas interactivos o tablas y descargar datos vectoriales en distintos formatos.

---

## Funcionalidades

### Exploración de servicios

* Conexión a servidores WMS y WFS.
* Consulta de títulos y resúmenes.
* Medición de latencia de los servicios.

### Catálogo de organismos

* Catálogo local editable.
* Búsqueda instantánea.
* Incorporación de nuevos organismos.
* Carga automática de URLs WMS y WFS.

### Visualización cartográfica

* Visualización de capas WMS.
* Visualización de capas WFS.
### Descarga de información geográfica

Exportación de capas WFS en:
* GeoJSON
* Shapefile (ZIP)
* KML
* GeoPackage (GPKG)

### Auditoría de atributos

* Visualización tabular.
* Detección de registros duplicados.
* Detección de campos vacíos.
* Evaluación de completitud.
* Búsquedas y filtros.

### Generación de informes

* Reportes PDF.
* Exportación a Excel (.xlsx).

---

## Instalación

### Opción 1: Ejecutable

1. Descargue la última versión desde la sección **Releases**.
2. Descomprima el archivo ZIP.
3. Mantenga los archivos:

```
WMS_WFS.exe
catalogo.json
```

en la misma carpeta.

4. Ejecute `WMS_WFS.exe`.

### Opción 2: Desde código fuente

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la aplicación:

```bash
python WMS_WFS.py
```

---

## Estructura del catálogo

El archivo `catalogo.json` almacena los organismos disponibles para consulta.

Ejemplo:

```json
{
    "Organismo": "Nombre del Organismo",
    "WMS": "https://servidor/geoserver/wms",
    "WFS": "https://servidor/geoserver/wfs"
}
```
