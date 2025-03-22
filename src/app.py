import streamlit as st
from pyvis.network import Network
import tempfile
import os
from db_interface import query_entity_graph, query_articles

st.set_page_config(layout="wide")
st.title("🕵️ Investigative Article Search")

articles = None

# Initialize session state
if "search_triggered" not in st.session_state:
    st.session_state.search_triggered = False

# --- HOMEPAGE ---
if not st.session_state.search_triggered:
    st.subheader("Search your article network")

    user_query = st.text_input("🔍 Enter search terms (e.g., 'Epstein')", "")
    if st.button("Search"):
        st.session_state.search_triggered = True
        st.session_state.last_query = user_query  # store for future use
        articles = query_articles(user_query)
        entity_graph = query_entity_graph(user_query)
        

# --- RESULTS PAGE ---
if st.session_state.search_triggered:
    st.subheader(f"🔎 Results for: {st.session_state.last_query}")

    col1, col2 = st.columns([1, 2])

    # --- Left: Dummy Article List ---
    with col1:
        st.markdown("### 📰 Articles")
        for title in articles:
            st.markdown(f"- {title}")

    # --- Right: Dummy Graph ---
    with col2:
        st.markdown("### 🌐 Semantic Network")

        net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white")
        net.from_nx(entity_graph)

        tmp_dir = tempfile.gettempdir()
        output_path = os.path.join(tmp_dir, "graph.html")
        net.save_graph(output_path)

        with open(output_path, "r", encoding="utf-8") as f:
            html = f.read()
        st.components.v1.html(html, height=500, scrolling=True)

    # Optionally add a back button
    st.button("🔙 New Search", on_click=lambda: st.session_state.update({"search_triggered": False}))
