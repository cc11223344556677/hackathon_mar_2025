import networkx as nx
import sqlite3
import json

# list of people (vertices)
# relevance score for each person based on how relevant they are in the article (for search)
# relationships between people (edges)
# descriptors of relationships

def get_results(search_query: str, dataset):
    res = dataset.execute(
        f"SELECT {search_query} FROM entities INNER JOIN relationships ON (entities.entity_name=relationships.start_node OR entities.entity_name=relationships.end_node)")
    return res

def query_entity_graph(search_query: str):
    '''
    Queries the SQLite database to find articles and associated named entities
    that match the user's search terms. Constructs and returns a semantic 
    NetworkX graph where nodes represent articles and entities, and edges 
    indicate which entities appear in which articles.

    Returns:
        networkx.Graph: A bipartite graph of articles and named entities.
    '''
    conn = sqlite3.connect('../entities_relationships.db')
    dataset = conn.cursor()
    results = dataset.execute(f"SELECT start_node, end_node, relationship_descriptor FROM relationships WHERE start_node='{search_query}' OR end_node='{search_query}'")

    G = nx.Graph()
    for result in results:
        G.add_edge(result[0], result[1], connection=result[2])

    # G.add_edge("Trump", "Melanie", connection="Husband-Wife")
    return G


def query_articles(search_query: str):
    '''
    Queries the SQLite database and retrieves a list of article titles 
    that match the user's search criteria.

    Returns:
        list[tuple]: A list of (title, publishment_date) tuples.
    '''
    conn = sqlite3.connect('../entities_relationships.db')
    dataset = conn.cursor()
    results = dataset.execute(
        "SELECT start_node, end_node, referenced_in_articles FROM relationships WHERE start_node=? OR end_node=?",
        (search_query, search_query)
    )

    article_ids = set()
    for row in results:
        article_ids.update(json.loads(row[2]))

    # Optional: add a manual article ID
    # article_ids.add("3d9e4333-8cd9-489d-a5e3-be617b52acb3")

    articles = []
    for article_id in article_ids:
        article_data = dataset.execute(
            "SELECT title, publishment_date FROM articles WHERE id=?", (article_id,)
        ).fetchone()
        if article_data:
            articles.append(article_data)

    conn.close()
    return articles