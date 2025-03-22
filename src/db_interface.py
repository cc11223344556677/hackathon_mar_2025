import networkx as nx

def query_entity_graph():
    '''
    Queries the SQLite database to find articles and associated named entities
    that match the user's search terms. Constructs and returns a semantic 
    NetworkX graph where nodes represent articles and entities, and edges 
    indicate which entities appear in which articles.

    Returns:
        networkx.Graph: A bipartite graph of articles and named entities.
    '''
    pass

def query_articles():
    '''
    Queries the SQLite database and retrieves a list of article titles 
    that match the user's search criteria.

    Returns:
        list[str]: A list of article titles.
    '''
    pass