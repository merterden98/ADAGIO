import networkx as nx
from dictionaries import Dict
from abc import ABC, abstractmethod, abstractproperty
from networkx.linalg.graphmatrix import adjacency_matrix
from t_map.gene.gene import Gene
from typing import Union, Tuple, Set, Any, Dict
import dataclasses
import numpy as np
from numpy.linalg import inv


@dataclasses.dataclass
class Description:
	requires_training: bool;
	##training_opts: TrainingOptions; # Hummus should know about TrainingOptions
	hyper_params: Dict[str, Any]

class Feta(ABC):
	@abstractproperty
	def description(self) -> Description:
		...
	@abstractmethod
	def prioritize(self, disease_gene: Gene, graph: Union[nx.Graph, None]) -> Set[Tuple[Gene, float]]:
		# In theory a model need not store the Graph and thus should rely on the Data library to pass it.
		...
	def __call__(self, disease_gene, graph: Union[nx.Graph, None]) -> Set[Tuple[Gene, float]]:
		return self.prioritize(disease_gene, graph)


class RandomWalkWithRestart(Feta):

	def __init__(self, hyper_params):
		self._desc = Description(requires_training=False, training_opts=None, hyper_params=hyper_params)
	def description(self) -> Description:
		return self.__desc
	def prioritize(self, disease_gene: Gene, graph: Union[nx.Graph, None]) -> Set[Tuple[Gene, float]]:
		# page rank function in networkx 
		pr = nx.pagerank(graph, self.__desc.hype_params, disease_gene)
		return pr


class PreComputeFeta(Feta):
	@abstractmethod
	def setup(self, graph: nx.Graph, *args, **kwargs):
		G = ([1, 2, 3], [2, 3, 4], [3, 4, 5]);
		A = adjacency_matrix(G)
		markov = np.array(A)
		markov = markov/markov.sum(axis = 0)
		inverse_matrix = np.inv(markov)
		I = np.identity(len(markov))
		# s = c(I - (1-c)markov)^-1r
		
		s = 0.85 (I - (0.15) * inverse_matrix) * self.__desc.hype_params
		
		
		


