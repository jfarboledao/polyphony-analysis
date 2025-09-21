
usuario = "admin"
password = "admin123"

from pymongo.mongo_client import MongoClient

uri = f'mongodb+srv://{usuario}:{password}@music-project.os8wuk4.mongodb.net/?retryWrites=true&w=majority&appName=Music-project'

client = MongoClient(uri, tls=True)

db = client['MUSIC']

# Seleccionar una coleccin
collectionKERN = db['KERN']
collectionMXML = db['MXML']
