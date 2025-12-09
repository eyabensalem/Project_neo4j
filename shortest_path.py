
import streamlit as st
import pandas as pd
import networkx as nx
from neo4j import GraphDatabase
import matplotlib.pyplot as plt

from dotenv import load_dotenv
import os

load_dotenv()
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# --- Charger graphe depuis Neo4j ---
def load_graph():
    query = "MATCH (c1:City)-[r:CONNECTED]->(c2:City) RETURN c1.name AS city1, c2.name AS city2, r.distance AS distance"
    with driver.session() as session:
        result = session.run(query)
        edges = [(record["city1"], record["city2"], record["distance"]) for record in result]
    G = nx.Graph()
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    return G

# --- Calculer shortest path ---
def get_shortest_path(G, source, target):
    path = nx.shortest_path(G, source=source, target=target, weight="weight")
    distances = [G[path[i]][path[i+1]]['weight'] for i in range(len(path)-1)]
    total_distance = sum(distances)
    return path, distances, total_distance

# --- Streamlit ---
st.title("Cities Shortest Path Dashboard")

G = load_graph()
cities = list(G.nodes)

source_city = st.selectbox("Source city", cities)
target_city = st.selectbox("Target city", cities)

if st.button("Compute Shortest Path"):
    if source_city != target_city:
        path, distances, total_distance = get_shortest_path(G, source_city, target_city)
        st.write(f"**Shortest path:** {' → '.join(path)}")
        st.write(f"**Distances between nodes:** {distances}")
        st.write(f"**Total distance:** {total_distance} km")

        # --- Visualiser le graphe et le chemin ---
        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(8,6))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, edge_color='gray')
        # mettre en évidence le chemin
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
        st.pyplot(plt)
    else:
        st.warning("Source et target doivent être différentes !")
