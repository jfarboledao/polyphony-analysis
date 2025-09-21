from conexion import collectionKERN, collectionMXML
from pprint import pprint
from pathlib import Path
import hashlib
from music21 import converter
import xml.etree.ElementTree as ET
from table import mostrarTabla

def parse_humdrum(file_path):
    metadata = {}
    data_lines = []
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('!!!'):
                key, value = line[3:].split(':', 1)
                metadata[key.strip()] = value.strip()
            elif not line.startswith('!!'):  # skip local comments
                data_lines.append(line.split('\t'))
    return metadata, data_lines

def es_nota_kern(token):
    if not token or token.startswith(('*', '=', '!', 'r')):
        return False
    if 'r' in token:
        return False
    return any(c.isalpha() for c in token)

def contar_notas_krn(file_path):
    contador = 0
    with open(file_path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('!') or line.startswith('*') or line.startswith('=') or not line:
                continue
            tokens = line.split('\t')
            for token in tokens:
                if es_nota_kern(token):
                    contador += 1
    return contador

def analizar_musicxml(archivo):
    score = converter.parse(archivo)
    num_notas = len([n for n in score.recurse().notes])
    metadata = score.metadata

    # Extraer título directamente desde el XML
    try:
        tree = ET.parse(archivo)
        root = tree.getroot()
        movement_title = root.find('movement-title')
        titulo = movement_title.text if movement_title is not None else "Sin título"
    except:
        titulo = metadata.title if metadata else "Sin título"

    newObject = {
        "autor": metadata.composer if metadata else "Desconocido",
        "titulo": titulo,
        "metadata": {
            "title": titulo,
            "composer": metadata.composer if metadata else "Desconocido"
        },
        "numeroNotas": num_notas
    }

    return newObject

def analizarDatos(archivo):
    extension = Path(archivo).suffix.lower()

    if extension == ".krn":
        file_path = f'{archivo}'
        metadata, _ = parse_humdrum(file_path)
        num_notas = contar_notas_krn(file_path)

        data = {}
        for k, v in metadata.items():
            data[k] = v

        # Buscar posibles campos de título en el archivo .krn
        posibles_titulos = [
            data.get('OTL'),   # Título principal
            data.get('TTL'),   # Título alternativo
            data.get('TITL'),  # Otra variante de título
            data.get('TITLE'), # Variante en inglés
            data.get('OTL@@DE'), # Título en alemán
            data.get('OPR'),   # Obra
            data.get('SCT'),   # Sección
            data.get('SUB'),   # Subtítulo
            data.get('COM'),   # Compositor (a veces usado como título)
        ]
        # Elegir el primer título no vacío
        titulo = next((t for t in posibles_titulos if t and t.strip()), "Sin título")

        # Buscar posibles campos de autor en el archivo .krn
        posibles_autores = [
            data.get('COM'),    # Compositor
            data.get('AUT'),    # Autor
            data.get('COMPOSER'), # Variante en inglés
            data.get('ARR'),    # Arreglista
            data.get('EDT'),    # Editor
            data.get('SRC'),    # Fuente (a veces contiene autor)
        ]
        # Elegir el primer autor no vacío
        autor = next((a for a in posibles_autores if a and a.strip()), "Desconocido")

        posibles_catalogos = [
            data.get("SCT"),
            data.get('BWV'),    # Bach-Werke-Verzeichnis (para Bach)
            data.get('CAT'),    # Catálogo
            data.get('CATALOG'), # Variante en inglés
            data.get('KOC'),    # Köchel (para Mozart)
            data.get('HOB'),    # Hoboken (para Haydn)
            data.get('D'),      # Deutsch (para Schubert)
            data.get('OP'),     # Opus
        ]

        catalogo = next((c for c in posibles_catalogos if c and c.strip()), "Desconocido")

        newObject = {
            "autor": autor,
            "titulo": titulo,
            "catalogo": catalogo,
            "metadata": data,
            "numeroNotas": num_notas
        }
        return newObject

    elif extension == ".musicxml":
        return analizar_musicxml(archivo)

    else:
        raise ValueError(f"Formato de archivo no soportado: {extension}")

def insertarDatos(carpeta):
    def ya_existe_en_db(hash_archivo):
        return collectionKERN.find_one({'hash': hash_archivo}) is not None

    def calcular_hash(archivo):
        with open(archivo, 'rb') as f:
            contenido = f.read()
            return hashlib.md5(contenido).hexdigest()

    file_path = Path(carpeta)

    # Buscar recursivamente archivos .krn y .musicxml en todas las subcarpetas
    for archivo in file_path.rglob('*'):
        if archivo.is_file() and archivo.suffix.lower() in [".krn", ".musicxml"]:
            hash_archivo = calcular_hash(archivo)

            if ya_existe_en_db(hash_archivo):
                print(f"El archivo {archivo} ya existe en la base de datos.")
                continue

            newObject = analizarDatos(archivo)
            newObject['hash'] = hash_archivo

            if archivo.suffix.lower() in [".krn"]:
                resultado = collectionKERN.insert_one(newObject)
            elif archivo.suffix.lower() in [".musicxml"]:
                resultado = collectionMXML.insert_one(newObject)
            print(f"El archivo {archivo} se insertó con el ID: {resultado.inserted_id}")


def llamarTabla(datos=[], columnas=None):
    mostrarTabla(datos, columnas)

def visualizarDatos():
    # Mostrar toda la información de la base de datos en la tabla y permitir filtrar columnas
    filas = []
    # Definir columnas a mostrar (puedes ajustar el orden o agregar más campos si lo deseas)
    columnas = ["_id", "autor", "titulo", "catalogo", "numeroNotas", "formato", "hash"]

    # Recopilar datos de collectionKERN
    for doc in collectionKERN.find():
        filas.append([
            str(doc.get("_id", "")),
            doc.get("autor", ""),
            doc.get("titulo", ""),
            doc.get("catalogo", "Desconocido"),
            doc.get("numeroNotas", 0),
            ".krn",
            doc.get("hash", "")
        ])
    # Recopilar datos de collectionMXML
    for doc in collectionMXML.find():
        filas.append([
            str(doc.get("_id", "")),
            doc.get("autor", ""),
            doc.get("titulo", ""),
            doc.get("catalogo", "Desconocido"),
            doc.get("numeroNotas", 0),
            ".musicxml",
            doc.get("hash", "")
        ])

    # Llamar a la tabla con opción de filtrar columnas
    llamarTabla(filas, columnas)


def eliminarDatos(tipoArchivo):

    filas = []
    if tipoArchivo == 1:
        #KERN
        for doc in collectionKERN.find():
            filas.append([
            str(doc.get("_id", "")),
            doc.get("autor", ""),
            doc.get("titulo", ""),
            doc.get("numeroNotas", 0),
            ".krn"
        ])
    elif tipoArchivo == 2:
        #MXML
        for doc in collectionMXML.find():
            filas.append([
            str(doc.get("_id", "")),
            doc.get("autor", ""),
            doc.get("titulo", ""),
            doc.get("numeroNotas", 0),
            ".krn"
        ])

    llamarTabla(filas)


