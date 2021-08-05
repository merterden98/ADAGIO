from t_map.gene.gene import Gene
from typing import Any, List, Set, Tuple, Union
from t_map.feta.description import Description
from t_map.feta.feta import PreComputeFeta
import networkx as nx
import numpy as np
from gfunc.command import glide_mat


class Glider(PreComputeFeta):

    def __init__(self, is_annotated=True, lamb: int = 1,
                 is_normalized: bool = False, glide_alph: float = 0.1,
                 glide_beta: int = 1000, glide_delta: int = 1,
                 glide_loc="cw_normalized") -> None:
        self.__desc = Description(requires_training=False, training_opts=False,
                                  hyper_params={
                                      "lamb": lamb,
                                      "is_normalized": is_normalized,
                                      "glide_alph": glide_alph,
                                      "glide_beta": glide_beta,
                                      "glide_delta": glide_delta,
                                      "glide_loc": glide_loc,
                                  })

    def description(self) -> Description:
        return self.__desc

    def setup(self, graph: nx.Graph, *args, **kwargs) -> Any:
        elist = list(graph.edges(data=True))
        elist = list(
            map(lambda x_y_z: (x_y_z[0], x_y_z[1], x_y_z[2]['weight']), elist))
        self.gmat, self.gmap = glide_mat(elist)
        self.rgmap = {self.gmap[key]: key for key in self.gmap}
        self.graph = self._update_edge_weights(graph, self.gmat, self.gmap)

    def _update_edge_weights(self, graph: nx.Graph, gmat: np.ndarray, gmap: dict) -> nx.Graph:
        for u, v in graph.edges():
            graph[u][v]['weight'] = gmat[gmap[u]][gmap[v]]
        return graph

    def prioritize(self, disease_genes: List[Gene],
                   graph: Union[nx.Graph, None]) -> Set[Tuple[Gene, float]]:

        personalization = dict()
        personalization = {gene.name: 1 for gene in disease_genes}
        pr = nx.pagerank(
            self.graph,
            alpha=0.85,
            personalization=personalization)
        data_set = set()

        for gene_id, score in pr.items():
            gene = Gene(name=gene_id)
            gene_pair = (gene, score)
            data_set.add(gene_pair)
        return data_set
