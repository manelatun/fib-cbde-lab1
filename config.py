postgres_config = "dbname=cbde user=cbde password=cbde"

# valores validos:
# euclidean_distance
# cosine_distance
order_by = "euclidean_distance"

limit = 5

frases_busqueda = [
  # Las 5 primeras se han escogido aleatoriamente de entre las 10.000 primeras frases del dataset bookcorpus,
  # Las otras 5 no se encuentran en el dataset y se han escrito para probar.
  # 2934
  "so i told her , and ever since i did she 's been bugging me to tell you too .",
  # 2062
  "and now half-ling , it whispered with joy , you die .",
  # 8942
  "he carried his dishes over to the sink , where later they would be washed by someone the khan hired to keep this place up .",
  # 4327
  "`` i tell you , the lord is healing me of my arthritis .",
  # 8308
  "i wanted to tell you , but i knew if i said too much i 'd get kicked out of the prism and i might never see you again `` gabriel bit his lip and looked over at alejo , annoyed .",

  "i'm really happy",

  "i'm really sorry",

  "am i sorry?",

  "what are you doing?",

  "feline",
]
