import networkx as nx


def gen_noise(graph: nx.Graph, percent: float = 0.05) -> nx.Graph:
    """
    Generate noise on the graph.
    :param graph:
    :return:

    # Given a percentage p of the edges to be added/removed in the network
    # 1) If p is less than 0 (removal):-> preserve the maximum spanning tree. For the remaining edges not in the tree,
    # sample from the uniform distribution $U$, for each edge in the network. If the u_{ij}
    # sampled for edge (i, j) is less than p, then remove.
    # If p is greater than 0 (addition) -> randomly generate [(p, q, w)] 
    """

    # TODO: Kapil
