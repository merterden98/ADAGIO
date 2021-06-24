import networkx as nx
from t_map.garbanzo.garbanzo import Garbanzo
from t_map.gene.gene import Gene


class EdgeListGarbanzo(Garbanzo):
    def __init__(self, graph_path: str, gene_path: str):
        self._graph = self._read_graph_from_path(graph_path)
        self._graph_path = graph_path
        self._gene_path = gene_path

    @property
    def graph(self) -> nx.Graph:
        return self._graph

    @property
    def graph_path(self) -> str:
        return self._graph_path

    @property
    def gene_path(self) -> str:
        return self._gene_path

    def get(self, i: int) -> Gene:
        raise NotImplementedError

    def _read_graph_from_path(self, path: str) -> nx.Graph:
        return nx.read_edgelist(path)
