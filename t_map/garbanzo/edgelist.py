import networkx as nx
from typing import List, Union, Set
from t_map.garbanzo.garbanzo import Garbanzo
from t_map.gene.gene import Gene


class EdgeListGarbanzo(Garbanzo):
    def __init__(self, graph_path: str, gene_path: str,
                 known_targets_path: Union[None, str] = None):
        self._graph_path = graph_path
        self._gene_path = gene_path
        self._graph = self._read_graph_from_path(graph_path)
        self._genes = self._read_genes_from_path(gene_path)
        if isinstance(known_targets_path, str):
            self._known_targets = self._read_genes_from_path(
                known_targets_path)
        else:
            self._known_targets = None

    @property
    def graph(self) -> nx.Graph:
        return self._graph

    @property
    def graph_path(self) -> str:
        return self._graph_path

    @property
    def gene_path(self) -> str:

        return self._gene_path

    @property
    def known_targets(self) -> Set[Gene]:
        if self._known_targets is None:
            return set()
        else:
            return set(self._known_targets)

    def __len__(self) -> int:
        return len(self._genes)

    def get(self, i: int) -> Gene:
        return self._genes[i]

    def _read_graph_from_path(self, path: str) -> nx.Graph:
        return nx.read_edgelist(path)

    def _read_genes_from_path(self, path: str) -> List[Gene]:
        genes = []
        with open(path) as f:
            for line in f.readlines():
                gene = line.strip()
                genes.append(Gene(name=gene))
        return genes
