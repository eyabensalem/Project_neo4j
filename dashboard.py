import streamlit as st
import requests

st.title("Chemin le plus court entre deux villes")

start = st.text_input("Ville de départ", "Paris")
end = st.text_input("Ville d'arrivée", "Lyon")

if st.button("Calculer"):
    url = f"http://127.0.0.1:5000/shortest_path?start={start}&end={end}"
    try:
        res = requests.get(url).json()
        if "error" in res:
            st.error(res["error"])
        else:
            st.success(f"Chemin: {' → '.join(res['path'])}")
            st.info(f"Distance totale: {res['distance']} km")
    except Exception as e:
        st.error(f"Impossible de se connecter à l'API: {e}")
