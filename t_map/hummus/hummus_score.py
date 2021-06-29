from typing import Union, List, Tuple, Callable, Iterable
from t_map.gene.gene import Gene

ScoreFn = Callable[Union[List[Gene], List[Tuple[Gene, float]]], None]


class HummusScore:
    def __init__(self, score_type: str = "top_k", k: int = 20):
        self._training = False

    def train(self) -> None:
        self._training = True

    def test(self) -> None:
        self._training = False

    def score(self, ground_truth: Iterable[Gene],
              scores: Union[List[Gene], List[Tuple[Gene, float]]]) -> None:
        ...
