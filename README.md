# Logica Matematica
## Proyecto 2

El proyecto esta formado por lo siguiente:
- Una base de datos basada en nodos (Neo4j) que inicialmente tiene:
  ### Nodos
  * Movie {title, year, duration, country}
  * User {name}
  * Person {name}
  * Productor {name}
  * Genre {name}

  ### Relaciones
  * User -[:LIKED]-> Movie
  * Person -[:ACTED_IN]-> Movie
  * Movie -[:IN_GENRE]-> Genre
  * Person -[:DIRECTED]-> Movie
  * Productor -[:PRODUCED]-> Movie

- Algortimo de recomendacion a partir de una pelicula el cual esta basado en el algoritmo de Jaccard.

Para instalar este programa se debe:
1. Instalar Python Neo4j por medio de la terminal (pip3 install neo4j)
2. Crear la base de datos en la aplicacion de Neo4j Desktop y colocarle la contraseña 'admin'.
3. Ejecutar el script con python 3


* Nota: La primera opcion del menu carga la base de datos en Neo4J, pero debe haberse creado e iniciado en Neo4J Desktop para conectarse.

## Shortest Path query:
  MATCH (initial {name: 'Pixar'}), (final {name: 'Walt Disney'}), path = shortestPath((initial)-[*]-(final)) WITH path WHERE length(path)> 1 RETURN path;
  
  ### Ejemplos
  MATCH (initial {name: 'Paramount Pictures'}), (final {name: 'Pixar'}), path = shortestPath((initial)-[*]-(final)) WITH path WHERE length(path)> 1 RETURN path
  
  MATCH (initial {name: 'Suspenso'}), (final {name: 'Epico'}), path = shortestPath((initial)-[*]-(final)) WITH path WHERE length(path)> 1 RETURN path
  
  MATCH (initial {name: 'Ciencia Ficcion'}), (final {name: '20th Century Fox'}), path = shortestPath((initial)-[*]-(final)) WITH path WHERE length(path)> 1 RETURN path
  
  MATCH (initial {name: 'M6'}), (final {name: '20th Century Fox'}), path = shortestPath((initial)-[*]-(final)) WITH path WHERE length(path)> 1 RETURN path
