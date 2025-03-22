import streamlit as st
from pyvis.network import Network
import tempfile
import os
import networkx as nx
import matplotlib.pyplot as plt
from db_interface import query_entity_graph, query_articles

st.set_page_config(layout="wide")
st.title("🕵️ Investigative Article Search")

articles = None
entity_graph = None

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
        st.session_state.articles = articles
        st.session_state.entity_graph = entity_graph

# --- RESULTS PAGE ---
if st.session_state.search_triggered:
    st.subheader(f"🔎 Results for: {st.session_state.last_query}")
    articles = st.session_state.articles
    entity_graph = st.session_state.entity_graph

    col1, col2 = st.columns([1, 2])

    # --- Left: Article List ---
    with col1:
        st.markdown("### 📰 Articles")
        for title in articles:
            st.markdown(f"- {title[0]}; {title[1]}")

    # --- Right: Graph Visualization with Centrality ---
    with col2:
        st.markdown("### 🌐 Semantic Network (colored by centrality)")

        # Select centrality type (None = default)
        centrality_option = st.selectbox(
            "Select centrality measure for coloring:",
            ("None", "Degree Centrality", "Betweenness Centrality", "Eigenvector Centrality")
        )

        # Compute centrality if selected
        if centrality_option == "Degree Centrality":
            centrality = nx.degree_centrality(entity_graph)
            centrality_label = "Degree"
        elif centrality_option == "Betweenness Centrality":
            centrality = nx.betweenness_centrality(entity_graph, normalized=True)
            centrality_label = "Betweenness"
        elif centrality_option == "Eigenvector Centrality":
            try:
                centrality = nx.eigenvector_centrality(entity_graph, max_iter=1000)
            except nx.PowerIterationFailedConvergence:
                centrality = {node: 0 for node in entity_graph.nodes()}
            centrality_label = "Eigenvector"
        else:
            centrality = None
            centrality_label = "None"

        # Setup Pyvis network
        net = Network(height="500px", width="100%", bgcolor="#222222", font_color="white")

        # Colormap
        cmap = plt.cm.coolwarm
        max_c = max(centrality.values()) if centrality else 1.0
        min_c = min(centrality.values()) if centrality else 0.0

        # Add nodes
        for node in entity_graph.nodes():
            if centrality:
                score = centrality.get(node, 0)
                norm_score = (score - min_c) / (max_c - min_c + 1e-5)
                rgba = cmap(norm_score)
                rgb = tuple(int(255 * c) for c in rgba[:3])
                color = f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})"
                title = f"{centrality_label} Centrality: {score:.2f}"
            else:
                color = "#cccccc"
                title = "No centrality coloring"

            net.add_node(
                node,
                label=node,
                title=title,
                color=color
            )

        # Add edges
        for u, v, data in entity_graph.edges(data=True):
            connection = data.get("connection", "No description")
            net.add_edge(u, v, title=connection)


        # Render to HTML
        tmp_dir = tempfile.gettempdir()
        output_path = os.path.join(tmp_dir, "graph.html")
        net.save_graph(output_path)

        with open(output_path, "r", encoding="utf-8") as f:
            html = f.read()
        st.components.v1.html(html, height=500, scrolling=True)

    # Optional reset button
    st.button("🔙 New Search", on_click=lambda: st.session_state.update({"search_triggered": False}))
