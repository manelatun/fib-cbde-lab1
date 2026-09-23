# Chroma, se insertan en batches

import chromadb
import statistics
import time
import json

from config import order_by

# https://docs.trychroma.com/docs/overview/getting-started
chroma_client = chromadb.PersistentClient(path="./chroma.db")
try:
  chroma_client.delete_collection(name="sentences")
except:
  pass

# CromaDB no permite modificar la formula de distancia despues de crear la coleccion,
# por lo que hay que volver a ejecutar este script si se modifica order_by
# https://docs.trychroma.com/docs/collections/configure#hnsw-index-configuration
if order_by == "euclidean_distance":
  chromadb_space = "l2"
elif order_by == "cosine_distance":
  chromadb_space = "cosine"
else:
  raise Exception(order_by + " no es valido")

collection = chroma_client.create_collection(
  name="sentences",
  configuration={
    "hnsw": {
      "space": chromadb_space,
    }
  }
)

print("Cargando embeddings.json")

# carga los embeddings desde el fichero ("simulamos" que los estamos generando)
start = time.perf_counter()
with open('embeddings.json', 'r') as f:
  result = json.load(f)
end = time.perf_counter()
load_time = end - start

print(f"{result['count']} embeddings, generados originalmente en {result['elapsed']} (Cargados en {load_time})")
print()
print("Subiendo a Chroma")

ids = [str(row['id']) for row in result['rows']]
sentences = [row['sentence'] for row in result['rows']]
embeddings = [row['embedding'] for row in result['rows']]

batch_size = 5000

times = []

# inserta los embedddings de cada frase del dataset en Chroma
for i in range(0, len(ids), batch_size):

  start = time.perf_counter()

  # https://docs.trychroma.com/docs/collections/add-data#adding-data
  collection.add(
    ids=ids[i:i+batch_size],
    documents=sentences[i:i+batch_size],
    embeddings=embeddings[i:i+batch_size]
  )

  end = time.perf_counter()
  times += [end - start]

# output de los tiempos de inserción (por batch)
print("Mean:", statistics.mean(times))
print("Median:", statistics.median(times))
print("Standard deviation:", statistics.stdev(times))
print("Min:", min(times))
print("Max:", max(times))
print("Total:", sum(times))
print("Batch size:", batch_size)
