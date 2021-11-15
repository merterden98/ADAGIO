from t_map.gene.gene import Gene
from typing import Any, List, Set, Tuple, Union, Optional
from t_map.feta.description import Description
from t_map.feta.feta import PreComputeFeta
from t_map.feta.dada import Dada
from t_map.feta.randomwalk import RandomWalkWithRestart
from t_map.garbanzo.transforms.tissue_reweight import reweight_graph_by_tissue
import networkx as nx
import numpy as np
from gfunc.command import glide_mat

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Glider(PreComputeFeta):

    def __init__(self, is_annotated=True, lamb: int = 1,
                 is_normalized: bool = False, glide_alph: float = 0.1,
                 glide_beta: int = 1000, glide_delta: int = 1,
                 with_dada: bool = False, dada_alpha: float = 0.85,
                 glide_loc="cw_normalized",  **kwargs) -> None:
        self.__desc = Description(requires_training=False, training_opts=False,
                                  hyper_params={
                                      "lamb": lamb,
                                      "is_normalized": is_normalized,
                                      "glide_alph": glide_alph,
                                      "glide_beta": glide_beta,
                                      "glide_delta": glide_delta,
                                      "glide_loc": glide_loc,
                                  })
        if with_dada:
            self.__dada = Dada(alpha=dada_alpha)

    def description(self) -> Description:
        return self.__desc

    def setup(self, graph: nx.Graph, *args, **kwargs) -> Any:
        elist = list(graph.edges(data=True))
        try:
            elist = list(
                map(lambda x_y_z: (x_y_z[0], x_y_z[1], x_y_z[2]['weight']), elist))
        except KeyError as e:
            print(bcolors.WARNING + "Warning: Could not detect edgeweights, defaulting to 1." + bcolors.ENDC)
            elist = list(
                map(lambda x_y_z: (x_y_z[0], x_y_z[1], 1), elist))

        self.gmat, self.gmap = glide_mat(elist, self.description().hyper_params)
        self.rgmap = {self.gmap[key]: key for key in self.gmap}
        self.graph = self._update_edge_weights(graph, self.gmat, self.gmap)

    def _update_edge_weights(self, graph: nx.Graph,
                             gmat: np.ndarray,
                             gmap: dict) -> nx.Graph:
        for u, v in graph.edges():
            graph[u][v]['weight'] = gmat[gmap[u]][gmap[v]]
        return graph

    def prioritize(self, disease_genes: List[Gene],
                   graph: Union[nx.Graph, None], tissue_file: Optional[str] = None, **kwargs) -> Set[Tuple[Gene, float]]:

        if tissue_file:
            graph = reweight_graph_by_tissue(graph, tissue_file)

        if hasattr(self, '__dada'):
            return self.__dada.prioritize(disease_genes, self.graph)
        else:
            rwr = RandomWalkWithRestart(alpha=0.85)
            return rwr.prioritize(disease_genes, self.graph)
