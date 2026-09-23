# PostgreSQL, se calcula la distancia en la aplicación

import psycopg2
from scipy.spatial.distance import euclidean, cosine
from prettytable import PrettyTable
import time
import statistics

from lib.do_embeddings import do_embeddings
from config import frases_busqueda, order_by, limit

# https://www.psycopg.org/docs/usage.html
conn = psycopg2.connect(dbname="cbde", user="cbde", password="cbde")
cur = conn.cursor()

times = []

# obtiene los embeddings de cada frase de búsqueda
for search in do_embeddings(frases_busqueda)['rows']:

  start = time.perf_counter()

  # obtiene todas las frases y embeddings guardados en PostgreSQL y calcula sus distancias
  cur.execute("SELECT * FROM sentences")
  rows = []
  for id, sentence, embeddings in cur.fetchall():
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.euclidean.html
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cosine.html
    rows.append((id, euclidean(search['embedding'], embeddings), cosine(search['embedding'], embeddings), sentence))

  # ordena los resultados por distancia
  def key_euclidean(row):
    return row[1]

  def key_cosine(row):
    return row[2]

  if order_by == "euclidean_distance":
    rows.sort(key=key_euclidean);
  elif order_by == "cosine_distance":
    rows.sort(key=key_cosine);
  else:
    raise Exception(order_by + " no es valido")

  # limita la cantidad de resultados
  rows = rows[:limit]

  end = time.perf_counter()

  times.append(end - start)

  # output de los resultados de la búsqueda
  print("Search:", search['sentence'])
  print("Time:", end - start)
  table = PrettyTable()
  table.field_names = ["id", "euclidean_distance", "cosine_distance", "sentence"]
  table.align = "l"
  table.add_rows(rows)
  print(table)
  print()

# output de los tiempos de búsqueda
print("Mean:", statistics.mean(times))
print("Median:", statistics.median(times))
print("Standard deviation:", statistics.stdev(times))
print("Min:", min(times))
print("Max:", max(times))
print("Total:", sum(times))
