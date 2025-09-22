# Analizador de Archivos Musicales KERN y MusicXML

Una aplicación Python con interfaz gráfica para el análisis musical de archivos KERN y MusicXML, enfocada en el conteo de intervalos y análisis de voice leading.

## Características

- **Análisis de archivos musicales**: Soporte para formatos KERN (.krn) y MusicXML (.musicxml)
- **Base de datos**: Almacenamiento y gestión de metadatos musicales
- **Conteo de intervalos**: Análisis de voice leading quartets
- **Interfaz gráfica**: Aplicación de escritorio desarrollada con Tkinter
- **Análisis masivo**: Procesamiento de múltiples archivos (Big Data)

## Funcionalidades

### Gestión de Datos
- Insertar datos musicales en la base de datos
- Visualizar datos almacenados
- Eliminar datos por tipo de archivo

### Análisis Musical
- **Conteo de intervalos por casos**: Análisis específico con entrada manual de notas
- **Análisis masivo**: Procesamiento automático de todos los archivos en la carpeta
- **Voice Leading**: Análisis de conducción de voces

## Estructura del Proyecto

```
├── main.py              # Interfaz gráfica principal
├── analizarKern.py      # Análisis de archivos KERN y MusicXML
├── conteoIntervalos.py  # Conteo de intervalos y voice leading
├── conexion.py          # Conexión a base de datos
├── table.py             # Visualización de tablas
├── vlqs.py              # Voice Leading Quartets
├── archivosKern/        # Archivos KERN de prueba
├── archivosMxml/        # Archivos MusicXML
└── archivosCompuesto/   # Archivos procesados
```

## Requisitos

- Python 3.x
- music21
- tkinter (incluido en Python)
- pymongo (para base de datos)
- MuseScore 4 (para renderizado musical)

## Instalación

1. Clona el repositorio
2. Instala las dependencias:
   ```bash
   pip install music21 pymongo
   ```
3. Asegúrate de tener MuseScore 4 instalado en tu sistema

## Uso

1. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

2. Utiliza la interfaz gráfica para:
   - Insertar archivos musicales en la base de datos
   - Visualizar los datos almacenados
   - Realizar análisis de intervalos
   - Procesar archivos masivamente

## Casos de Análisis

La aplicación incluye varios casos predefinidos para el análisis de intervalos:

- **Case 1**: Análisis de intervalos específicos (6ªm/6ªM → 8ª)
- **Case 2**: Análisis de terceras mayores a quintas perfectas
- **Case 3**: Análisis de tercera menor a unísono

## Contribuir

Este proyecto está en desarrollo activo. Las siguientes mejoras están planificadas:
- Implementación completa del conteo de intervalos
- Mejoras en la interfaz de usuario
- Optimización del filtrado de datos
- Integración en la nube para la base de datos
