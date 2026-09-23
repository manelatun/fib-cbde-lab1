# Búsqueda en Chroma, no se pueden hacer muchas variaciones

import chromadb
from prettytable import PrettyTable
import time
import statistics

from lib.do_embeddings import do_embeddings
from config import frases_busqueda, limit

# https://docs.trychroma.com/docs/overview/getting-started
chroma_client = chromadb.PersistentClient(path="./chroma.db")
collection = chroma_client.get_collection(name="sentences")

times = []

# obtiene los embeddings de cada frase de búsqueda
for search in do_embeddings(frases_busqueda)['rows']:

  start = time.perf_counter()

  # realiza la búsqueda de la frase actual
  # https://docs.trychroma.com/docs/querying-collections/query-and-get#query
  results = collection.query(
    query_embeddings=[search['embedding']],
    n_results=limit,
  )

  end = time.perf_counter()

  times.append(end - start)

  # output de los resultados de la búsqueda
  print("Search:", search['sentence'])
  print("Time:", end - start)

  # estructura el resultado de Chroma
  # https://docs.trychroma.com/docs/querying-collections/query-and-get#results-shape
  for ids, documents, distances in zip(results["ids"], results["documents"], results["distances"]):
    table = PrettyTable()
    table.field_names = ["id", "sentence", "distance"]
    table.align = "l"

    for id, document, distance in zip(ids, documents, distances):
      table.add_row([id, document, distance])

    print(table)
    print()

# output de los tiempos de búsqueda
print("Mean:", statistics.mean(times))
print("Median:", statistics.median(times))
print("Standard deviation:", statistics.stdev(times))
print("Min:", min(times))
print("Max:", max(times))
print("Total:", sum(times))
