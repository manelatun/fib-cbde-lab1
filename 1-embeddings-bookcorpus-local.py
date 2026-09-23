from datasets import load_dataset
import json

from do_embeddings import do_embeddings

# En local solo generamos embeddings para 1.000 frases.
# Los resultados se guardan en embeddings.json para poder usarlos posteriormente en el resto de scripts.

# carga el dataset, que tiene una única columna con la frases
# https://huggingface.co/docs/datasets/en/loading
dataset = load_dataset("SamuelYang/bookcorpus", split="train[:1000]")
sentences = dataset['text']

# calcula y guarda los embeddings
result = do_embeddings(sentences)
with open('embeddings.json', 'w') as f:
  json.dump(result, f)
