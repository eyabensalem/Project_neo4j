import pandas as pd
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def create_city(tx, city, population, region):
    tx.run(
        "MERGE (c:City {name: $name}) "
        "SET c.population = $population, c.region = $region",
        name=city, population=population, region=region
    )

def create_connection(tx, city1, city2, distance, transport):
    tx.run(
        """
        MATCH (a:City {name: $city1}), (b:City {name: $city2})
        MERGE (a)-[:CONNECTED {distance: $distance, transport: $transport}]->(b)
        MERGE (b)-[:CONNECTED {distance: $distance, transport: $transport}]->(a)
        """,
        city1=city1, city2=city2, distance=distance, transport=transport
    )

df = pd.read_csv("cities.csv")

with driver.session() as session:
    for _, row in df.iterrows():
        session.execute_write(create_city, row['city1'], row['city1_pop'], row['region1'])
        session.execute_write(create_city, row['city2'], row['city2_pop'], row['region2'])
        session.execute_write(create_connection, row['city1'], row['city2'], float(row['distance']), row['transport'])

print("✅ Import enrichi terminé !")
