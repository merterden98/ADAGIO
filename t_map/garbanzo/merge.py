import networkx as nx
from itertools import chain
from t_map.garbanzo.garbanzo import Garbanzo
from typing import Iterable, Union, List
from t_map.gene.gene import Gene


class MergedGarbanzo(Garbanzo):

    def __init__(self, graph: nx.Graph, genes: List[Gene]):
        self._graph = graph
        self._genes = genes

    @property
    def graph(self) -> nx.Graph:
        return self._graph

    @property
    def graph_path(self) -> str:
        raise Exception("Merged Graphs Do Not Have a graph path")

    @property
    def gene_path(self) -> str:
        raise Exception("Merged Graphs Do Not Have a gene path")

    @property
    def genes(self) -> List[Gene]:
        return self._genes

    def get(self, i: int) -> Gene:
        return self.gene_list[i]

    def __len__(self) -> int:
        return len(self.gene_list)


def merge(items: Iterable[Union[Garbanzo, nx.Graph]]) -> Garbanzo:

    if not any([isinstance(item, Garbanzo) for item in items]):
        raise Exception("At least one item needs to be of instance Garbanzo")

    garbanzos = [item for item in items if isinstance(item, Garbanzo)]
    garbanzo_graphs = [g.graph for g in garbanzos]
    garbanzo_genes = list(chain([g.genes for g in garbanzos]))
    graphs = [item for item in items if isinstance(item, nx.Graph)]
    merged_graph = nx.compose_all(list(chain(garbanzo_graphs, graphs)))
    return MergedGarbanzo(merged_graph, garbanzo_genes)
