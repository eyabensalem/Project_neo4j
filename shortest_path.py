# shortest_path.py
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv


load_dotenv()
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Connexion à Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def shortest_path_weighted(start_city, end_city):
    with driver.session() as session:
        query = """
        MATCH (start:City {name: $start_city}), (end:City {name: $end_city})
        CALL gds.shortestPath.dijkstra.stream({
            nodeProjection: 'City',
            relationshipProjection: {
                CONNECTED: {
                    type: 'CONNECTED',
                    properties: 'distance'
                }
            },
            startNode: start,
            endNode: end,
            relationshipWeightProperty: 'distance'
        })
        YIELD index, nodeIds, costs
        RETURN [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS path,
               reduce(total=0.0, c IN costs | total+c) AS total_distance
        """
        result = session.run(query, start_city=start_city, end_city=end_city)
        record = result.single()
        if record:
            return record["path"], record["total_distance"]
        else:
            return None, None

# Exemple d'utilisation
if __name__ == "__main__":
    path, distance = shortest_path_weighted("Paris", "Lyon")
    print("Chemin:", path)
    print("Distance totale:", distance)
