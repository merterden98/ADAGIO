import networkx as nx
from abc import ABC, abstractmethod, abstractproperty
from t_map.gene.gene import Gene
from typing import Union, Tuple, Set, List
from t_map.feta.description import Description

# There are two types of models: iterative and precompute
# For both the iterative and precompute method we have the following functions:
#
#		description: Returns a description of the model.
#					 Default: requires_training=False, training_opts=None, hyper_params={"alpha": alpha}
#																  where alpha = 0.85 (probabiltiy of restart)
#
#		prioritize: Prioritizes a set of genes in a graph based on random walk with restart algorithm
# 					Parameters: Takes in a list fo Genes
#								Optional: a networkx Graph
# 					Returns a set of tuples with the gene and a probability from 0 to 1 where 1 is the highest
#					probability of being associated with the known gene
#
#		call: Calls prioritization on either a singular gene or a list of genes
#			  Parameters:
#			  Returns a set of tuples with the gene and a probability from 0 to 1 where 1 is the highest
#					probability of being associated with the known gene
#			  Exceptions: call throws and exception if not given a gene or a list of genes
#
# For the precompute method we also have a setup function
#		setup: Creates the probability matrix based on the graph given
#			   Parameters: a networkx Graph
#			   Returns the probability matrix to prioritize so prioritize can use it
#


class Feta(ABC):
    @abstractproperty
    def description(self) -> Description:
        ...

    @abstractmethod
    def prioritize(self, disease_gene: List[Gene],
                   graph: Union[nx.Graph, None]) -> Set[Tuple[Gene, float]]:
        # In theory a model need not store the Graph and thus should rely on the Data library to pass it.
        ...

    def __call__(self, disease_gene: Union[Gene, List[Gene]],
                 graph: Union[nx.Graph, None]) -> Set[Tuple[Gene, float]]:
        if isinstance(disease_gene, Gene):
            return self.prioritize([disease_gene], graph)
        elif isinstance(disease_gene, list) and \
                all(isinstance(x, Gene) for x in disease_gene):
            return self.prioritize(disease_gene, graph)
        else:
            Exception(
                "Need to pass a Gene or a list of Genes, instead passed:",
                type(disease_gene))


class PreComputeFeta(Feta):
    @abstractmethod
    def setup(self, graph: nx.Graph, *args, **kwargs):
        ...
