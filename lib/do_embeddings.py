from sentence_transformers import SentenceTransformer
import time

# carga del transformer que usaremos para generar los embeddings de cada frase
# https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2#usage-sentence-transformers
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def do_embeddings(sentences):
  global model

  # genera los embeddings
  start = time.perf_counter()
  embeddings = model.encode(sentences)
  end = time.perf_counter()

  # metadatos
  count = embeddings.shape[0]
  dimensions = embeddings.shape[1]
  elapsed = end - start

  assert count == len(embeddings)
  assert count == len(sentences)
  assert dimensions == 384 # de momento, el tamaño del vector está hardcodeado en nuestra implementación

  rows = []
  for id in range(count):
    rows.append({
      "id": id,
      "sentence": sentences[id],
      "embedding": embeddings[id].tolist()
    })

  result = {
    "elapsed": elapsed,
    "count": count,
    "dimensions": dimensions,
    "rows": rows
  }

  return result
