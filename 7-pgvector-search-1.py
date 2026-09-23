# PostgreSQL, búsqueda con los procedimientos almacenados de distancia proporcionados pgVector, sin índices

import psycopg2
from prettytable import PrettyTable
import time
import statistics

# en este caso el query producía errores al intentar pasar una lista de python como parámetro
# https://pypi.org/project/pgvector/#user-content-psycopg-2
from pgvector.psycopg2 import register_vector
from pgvector import Vector

from lib.do_embeddings import do_embeddings
from config import frases_busqueda, order_by, limit, postgres_config

# https://www.psycopg.org/docs/usage.html
conn = psycopg2.connect(postgres_config)
register_vector(conn)
cur = conn.cursor()

# borra los índices si existen
cur.execute("DROP INDEX IF EXISTS index_hnsw_l2;")
cur.execute("DROP INDEX IF EXISTS index_hnsw_cosine;")
conn.commit()

times = []

# obtiene los embeddings de cada frase de búsqueda
for search in do_embeddings(frases_busqueda)['rows']:

  start = time.perf_counter()

  # obtiene todas las frases y embeddings guardados en PostgreSQL y calcula sus distancias
  # calcula las distancias, y ordena y limita el resultado directamente en el servidor de PostgreSQL
  # https://github.com/pgvector/pgvector#querying
  cur.execute(
    f"""
      SELECT
        id,
        embedding <-> %s AS euclidean_distance,
        embedding <=> %s AS cosine_distance,
        sentence
      FROM sentences_pgvector
      ORDER BY {order_by} ASC
      LIMIT {limit}
    """, (
      Vector(search['embedding']),
      Vector(search['embedding'])
    )
  )
  rows = cur.fetchall();

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
