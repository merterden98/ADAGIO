from __future__ import annotations
import networkx as nx
import random
from functools import partial
from t_map.garbanzo.garbanzo import Garbanzo
from typing import Iterator, List, Tuple, Union, Generator
from t_map.gene.gene import Gene
from t_map.hummus.hummus_score import HummusScore, ScoreFn
from math import floor
from sklearn.model_selection import KFold


class Hummus:

    def __init__(self, data: Garbanzo,
                 with_scoring: Union[None,
                                     HummusScore] = None,
                 train_test_split_ratio: float = 0.8):
        self.data = data
        self._genes = [self.data.get(i) for i in range(len(data))]
        self._score_module = with_scoring
        self._with_cv = False
        self._train_test_split_ratio = train_test_split_ratio

    def with_cv(self, k_fold=5) -> Hummus:
        self._with_cv = True
        self._k = k_fold
        self._kf = KFold(n_splits=self._k)
        return self

    def train(self) -> HummusTrainer:
        '''
            checks if a _k has been set, if not
            will initialize a default train split
        '''
        if self._with_cv is False:
            train_size = floor(len(self.data) * self._train_test_split_ratio)
            items = {i for i in range(len(self.data))}
            self._train = random.sample(items, k=train_size)
            self._test = list(items - set(self._train))

        return HummusTrainer(self.data, self._train, self._score_module)

    def test(self) -> HummusTester:
        # If the user hasn't selected cv mode and hasn't run the
        # training loop assume they want to test on whole dataset
        if self._with_cv is False and not hasattr(self, "_test"):
            self._test = [i for i in range(len(self.data))]

        return HummusTester(self.data, self._test, self._score_module)

    def __iter__(self) -> Generator[Tuple[HummusTrainer, HummusTester],
                                    None,
                                    None]:
        assert self._with_cv, f"{self} has not been set to cv mode"

        for (train, test) in self._kf.split(self._genes):
            self._train = train
            self._test = test
            yield (self.train(), self.test())


class HummusTester(Iterator):

    def __init__(self, data: Garbanzo, test_idx: List[int],
                 with_scoring: Union[None,
                                     HummusScore] = None):

        self._data: Garbanzo = data
        self._test: List[int] = test_idx
        self._i = 0
        self._with_scoring = with_scoring
        if self._with_scoring is not None:
            self._collect_known_genes()

    def _collect_known_genes(self):
        '''
            Will set self._known_targets to all the
            known disease/target genes. (perhaps we need
            to change this in the future)
        '''
        self._known_targets: List[Gene] = [
            self._data.get(i) for i in range(len(self._data))]

    def __next__(self) -> Union[Tuple[Gene, nx.Graph],
                                Tuple[Gene, nx.Graph, ScoreFn]]:

        if isinstance(self._with_scoring, HummusScore):
            self._with_scoring.test()

            if self._i < len(self._test):
                i = self._i
                score_fn = partial(self._with_scoring.score,
                                   self._known_targets, self._data.get(i))
                self._i += 1
                return (self._data.get(i), self._data.graph, score_fn)

        elif self._i < len(self._test):
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

        if self._with_scoring is not None:
            self._collect_known_genes()

    def _collect_known_genes(self):
        self._known_targets: List[Gene] = [
            self._data.get(i) for i in self._train]

    def __next__(self) -> Union[Tuple[Gene, nx.Graph],
                                Tuple[Gene, nx.Graph, ScoreFn]]:

        if isinstance(self._with_scoring, HummusScore):
            self._with_scoring.train()

            if self._i < len(self._train):
                i = self._i
                score_fn = partial(self._with_scoring.score,
                                   self._known_targets, self._data.get(i))
                self._i += 1
                return (self._data.get(i), self._data.graph, score_fn)

        elif self._i < len(self._train):
            i = self._i
            self._i += 1
            return (self._data.get(i), self._data.graph)

        raise StopIteration
