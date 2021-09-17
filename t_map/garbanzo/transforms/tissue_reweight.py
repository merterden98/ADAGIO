import networkx as nx


def reweight_graph_by_tissue(graph: nx.Graph,
                             file_path: str,
                             weight: float = 0.001) -> nx.Graph:
    """
    Given a network `graph` of ppi interactions, and a file path to containing data
    as to where or not a gene is expressed in a given tissue:
        ENSEMBL_ID   Gene	[0-1]
    where 0 indicates low expression and 1 indicates high expression. The function
    reweights the graph by multiplying the weight of each edge by w' = w * weight^{2 - n}
    where n is the number of highly expressed genes in the tissue.


    Parameters
    ----------
    graph : nx.Graph
        A networkx graph object representing the ppi network.
    file_path : str
        A string representing the path to the tissue gene file.
    weight : float, optional
        The weight to assign to each edge in the new graph.

    Returns
    -------
    nx.Graph
        A new networkx graph object with the same nodes and edges as the input
        graph, but with each edge weighted by the tissue-specific interaction
        frequency.
    """

    is_expressed = dict()
    # Read in the tissue-specific interaction file.
    with open(file_path, 'r') as f:
        for line in f:
            _, gene, is_expressed_str = line.split('\t')
            is_expressed[gene] = int(is_expressed_str)

    # Create a new graph with the same nodes and edges as the input graph.
    new_graph = nx.Graph()
    new_graph.add_nodes_from(graph.nodes())
    new_graph.add_edges_from(graph.edges())

    # Iterate through each edge in the new graph.
    for edge in new_graph.edges():
        new_graph[edge[0]][edge[1]]['weight'] = graph[edge[0]][edge[1]]['weight'] * \
            (weight ** (2 - is_expressed[edge[0]] - is_expressed[edge[1]]))

    return new_graph
