from typing import Union, List, Tuple, Callable, Iterable, Set
from t_map.gene.gene import Gene

ScoreFn = Callable[[Union[List[Gene], List[Tuple[Gene, float]]]], None]


class HummusScore:
    def __init__(self, score_type: str = "top_k", k: int = 20):
        self._score_type = score_type
        self._k = k
        self._training = False
        self._scores: List[dict] = []
        self._training_scores: List[List[dict]] = []
        self._testing_scores: List[List[dict]] = []
        self._ground_truth: Union[None, Set[Gene]] = None

    def train(self) -> None:
        if len(self._scores) > 0:
            self._testing_scores.append(self._scores)
            self._scores = []
        self._training = True

    def test(self) -> None:
        if len(self._scores) > 0:
            self._training_scores.append(self._scores)
            self._scores = []
        self._training = False

    def score(self, ground_truth: Iterable[Gene],
              disease_gene: Gene,
              predictions: Union[List[Gene],
                                 List[Tuple[Gene, float]]]) -> None:

        if self._ground_truth is None:
            self._ground_truth = set(ground_truth)

        if self._score_type == "top_k":
            '''
                If the user passes in a list of tuples ensure we
                sort it by score, otherwise we assume it is passed
                in sorted order
            '''
            if all(isinstance(v, tuple) for v in predictions):
                # need to do this for type checking :/
                new_predictions: List[Tuple[Gene, float]
                                      ] = predictions  # type: ignore
                sorted_predictions = sorted(
                    new_predictions,
                    key=lambda x: x[1],
                    reversed=True)  # type: ignore
                predictions = list(
                    map(lambda x: x[0], sorted_predictions))

            predictions = predictions[0:self._k]
            genes_in_ground_truth = len(list(filter(
                lambda x: x in self._ground_truth, predictions)))

            self._scores.append({"gene": disease_gene,
                                 "score": genes_in_ground_truth / self._k,
                                 "predictions": predictions})
            return
        else:
            raise Exception(
                f"{self._score_type} is not a valid score function")
