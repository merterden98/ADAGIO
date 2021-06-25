from __future__ import annotations
import networkx as nx
import random
from t_map.garbanzo.garbanzo import Garbanzo
from typing import Iterator, List, Tuple
from t_map.gene.gene import Gene


class Hummus:
    K_DEFAULT = 5

    def __init__(self, data: Garbanzo):
        self.data = data

    def with_cv(self, k_fold=5) -> Hummus:
        self._k = k_fold
        self._test_size = len(self.data) // self._k
        self._train_size = len(self.data) - self._test_size
        items = {i for i in range(len(self.data))}
        self._train = random.sample(items, k=self._train_size)
        self._test = list(items - set(self._train))
        return self

    def train(self) -> HummusTrainer:
        '''
            checks if a _k has been set, if not
            will initialize a default train split
        '''
        if not hasattr(self, '_k'):
            self.with_cv()
        return HummusTrainer(self.data, self._train)

    def test(self) -> HummusTester:
        raise NotImplementedError

    def __enter__(self) -> HummusTester:
        return self.test()

    def __exit__(self, value, traceback):
        return


class HummusTester(Iterator):
    ...


class HummusTrainer(Iterator):

    def __init__(self, data: Garbanzo, train_idx: List[int]):
        self._data: Garbanzo = data
        self._train: List[int] = train_idx
        self._i = 0

    def __next__(self) -> Tuple[Gene, nx.Graph]:

        if self._i < len(self._train):
            i = self._i
            self._i += 1
            return (self._data.get(i), self._data.graph)

        raise StopIteration
