# Proyecto 2 Logica Matematica
# Jose Block 18935
# Gian Luca Rivera 18049
# Francisco Rosal 18676

from neo4j import GraphDatabase

# Conexion a la base de datos
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "admin"))

def deleteLastDB(tx):
    # Elimina los nodos y conexiones existentes
    tx.run("MATCH (n) DETACH DELETE n")

def initTransaction(tx):
    # Lee el archivo que contiene
    file = open("db.txt", "r", encoding='utf-8')
    datab = file.read()
    tx.run(datab)
    file.close

def findMovieRelateTo(tx, movie):
    # Hace la busqueda en la base de datos a partir de una pelicula ingresada, se busca las mas similares a esta
    for movie in tx.run("""
        MATCH (movie:Movie) WHERE movie.title = $movie
        MATCH (movie:Movie)-[:IN_GENRE|:ACTED_IN|:PRODUCED|:DIRECTED]-(filtered)<-[:IN_GENRE|:ACTED_IN|:PRODUCED|:DIRECTED]-(recMovie:Movie)
        WITH movie, recMovie, COUNT(filtered) AS intersection

        MATCH (movie)-[:IN_GENRE|:ACTED_IN|:PRODUCED|:DIRECTED]-(mov)
        WITH movie, recMovie, intersection, COLLECT(mov.name) AS conjunto1
        MATCH (recMovie)-[:IN_GENRE|:ACTED_IN|:PRODUCED|:DIRECTED]-(re)
        WITH movie, recMovie, intersection, conjunto1, COLLECT(re.name) AS conjunto2

        WITH movie, recMovie, intersection, conjunto1, conjunto2, conjunto1 + filter(i IN conjunto2 WHERE NOT i IN conjunto1) AS union
        RETURN movie.title AS YouLike, recMovie.title AS Recommendation, conjunto1 AS Props1, conjunto2 AS Props2,
            ((1.0*intersection) / SIZE(union)) AS JaccardNumber
        ORDER BY JaccardNumber DESC LIMIT 15
    """, movie=movie):
        print(movie["Recommendation"])

def initDB():
    # Acciones que inician y reinician la db al correr el programa
    with driver.session() as session:
        session.write_transaction(deleteLastDB)
        session.write_transaction(initTransaction)

def findMovie(movie):
    with driver.session() as session:
        session.read_transaction(findMovieRelateTo, movie)

def shortestPathQuery(tx, key1, value1, key2, value2):
    # Hace la busqueda en el grafo para encontrar el camino mas corto entre dos nodos
    for record in tx.run("""
        MATCH (initial {%s: '%s'}), (final {%s: '%s'}),
            path = shortestPath((initial)-[*]-(final))
        WITH path
        WHERE length(path) > 1
        RETURN path;
    """ % (key1, value1, key2, value2)):
        nodes = record['path'].nodes

        for node in nodes:
            print(node)

def shortestPath(key1, value1, key2, value2):
    with driver.session() as session:
        session.read_transaction(shortestPathQuery, key1, value1, key2, value2)

def menu():
    print("""
        Menu:
    1. Load DB
    2. Shortest Path
    3. Find movie recommendation
    """)

continuar = True
while continuar:
    menu()
    opcion = input("Ingrese un numero: ")

    if opcion == '1':
        initDB()
    elif opcion == '2':
        print("Nodo inicial")
        key1 = input("\tIngrese una title/name: ")
        value1 = input("\tIngrese el titulo o nombre: ")
        print("Nodo final")
        key2 = input("\tIngrese una title/name: ")
        value2 = input("\tIngrese el titulo o nombre: ")
        shortestPath(key1, value1, key2, value2)
    elif opcion == '3':
        movie = input("Ingrese una pelicula: ")
        findMovie(movie)
    else:
        continuar = False
