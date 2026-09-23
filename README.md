1. Para generar los embeddings del dataset bookcorpus hay que ejecutar `1-embeddings-bookcorpus-colab.ipynb` o `1-embeddings-bookcorpus-local.py` que guardan el resultado en `embeddings.json`. El repositorio ya contiene un fichero `embeddings.json` con los embeddings de las primeras 100.000 frases de bookcorpus, por lo que **se puede omitir este paso**.

2. Modifica el fichero `config/postgresql.py` con la información de conexión a la base de datos.

   Ejemplo de como crear la base de datos:

   ```sh
   sudo -u postgres psql -U postgres -d postgres
   ```
   ```sql
   -- Crea el usuario y la base de datos
   CREATE ROLE cbde WITH LOGIN PASSWORD 'cbde';
   CREATE DATABASE cbde WITH OWNER cbde;
   -- Configura pgVector para más adelante
   \connect cbde
   CREATE EXTENSION vector;
   ```

3. Modifica el fichero `config/search.py` 
