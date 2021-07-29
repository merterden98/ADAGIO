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
                 glide_loc="cw_normalized", k=20) -> None:
        self.__desc = Description(requires_training=False, training_opts=False,
                                  hyper_params={
                                      "lamb": lamb,
                                      "is_normalized": is_normalized,
                                      "glide_alph": glide_alph,
                                      "glide_beta": glide_beta,
                                      "glide_delta": glide_delta,
                                      "glide_loc": glide_loc,
                                      "k": k
                                  })

    def description(self) -> Description:
        return self.__desc

    def setup(self, graph: nx.Graph, *args, **kwargs) -> Any:
        elist = list(graph.edges(data=True))
        elist = list(
            map(lambda x_y_z: (x_y_z[0], x_y_z[1], x_y_z[2]['weight']), elist))
        self.gmat, self.gmap = glide_mat(elist)
        self.rgmap = {self.gmap[key]: key for key in self.gmap}

    def find_most_likely(self, gene_name: str, k: int):
        """
        For a single gene
        """
        geneid = self.gmap[gene_name]
        scores = self.gmat[geneid]
        ids_sorted = np.argsort(scores * -1)[: k]
        return [(self.rgmap[id], scores[id]) for id in ids_sorted]

    def final_list(self, genes: List[Gene], k: int):
        gene_scores = {}
        for gene in genes:
            slist = self.find_most_likely(gene.name, k)
            for g, score in slist:
                if g not in gene_scores:
                    gene_scores[g] = 0
                gene_scores[g] += score
        gene_scores_l = [(key, gene_scores[key]) for key in gene_scores]
        return sorted(gene_scores_l, reverse=True, key=lambda x: x[1])

    def prioritize(self, disease_genes: List[Gene],
                   graph: Union[nx.Graph, None]) -> Set[Tuple[Gene, float]]:
        return set(self.final_list(disease_genes,
                                   self.__desc.hyper_params["k"]))
