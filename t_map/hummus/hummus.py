from __future__ import annotations
import networkx as nx
import random
from functools import partial
from t_map.garbanzo.garbanzo import Garbanzo
from typing import Iterator, List, Tuple, Union
from t_map.gene.gene import Gene
from t_map.hummus.hummus_score import HummusScore, ScoreFn


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
        raise HummusTester(self.data, self._test)

    def __enter__(self) -> HummusTester:
        return self.test()

    def __exit__(self, value, traceback):
        return


class HummusTester(Iterator):

    def __init__(self, data: Garbanzo, test_idx: List[int],
                 with_scoring: Union[None,
                                     HummusScore] = None):

        self._data: Garbanzo = data
        self._test: List[int] = test_idx
        self._i = 0
        self._with_scoring = with_scoring

    def __next__(self) -> Union[Tuple[Gene, nx.Graph],
                                Tuple[Gene, nx.Graph, ScoreFn]]:

        if isinstance(self._with_scoring, HummusScore):
            self._with_scoring.test()
            score_fn = partial(self._with_scoring.score,
                               self._data.known_targets)

            if self._i < len(self._train):
                i = self._i
                self._i += 1
                return (self._data.get(i), self._data.graph, score_fn)

        elif self._i < len(self._train):
            i = self._i
            self._i += 1
            return (self._data.get(i), self._data.graph)

        raise StopIteration


class HummusTrainer(Iterator):

    def __init__(self, data: Garbanzo, train_idx: List[int],
                 with_scoring: Union[None,
                                     HummusScore] = None):

        self._data: Garbanzo = data
        self._train: List[int] = train_idx
        self._i = 0
        self._with_scoring = with_scoring

    def __next__(self) -> Union[Tuple[Gene, nx.Graph],
                                Tuple[Gene, nx.Graph, ScoreFn]]:

        if isinstance(self._with_scoring, HummusScore):
            self._with_scoring.train()
            score_fn = partial(self._with_scoring.score,
                               self._data.known_targets)

            if self._i < len(self._train):
                i = self._i
                self._i += 1
                return (self._data.get(i), self._data.graph, score_fn)

        elif self._i < len(self._train):
            i = self._i
            self._i += 1
            return (self._data.get(i), self._data.graph)

        raise StopIteration
