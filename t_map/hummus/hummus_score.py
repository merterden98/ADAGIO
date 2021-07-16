from typing import Union, List, Tuple, Callable, Iterable, Set
from t_map.gene.gene import Gene
from enum import Enum, auto
import itertools

ScoreFn = Callable[[Union[List[Gene], List[Tuple[Gene, float]]]], None]


class ScoreTypes(Enum):
    TOP_K = auto()


class HummusScore:
    """Hummus Score is a module used for scoring a particular
    prioritization algorithm. Its main purpose is to be passed
    into an instance of Hummus to the `with_scoring` parameter.
    If provided during testing and training time, the Hummus
    module with additionally return a score function, which will
    accept a list of prediction with or without a score.

    Note: Hummus Score function returns None. It is the responsibility
    of Hummus Score to later provide results.
    """

    def __init__(self, score_type: ScoreTypes = ScoreTypes.TOP_K, k: int = 20):
        self._score_type = score_type
        self._k = k
        self._training = False
        self._scores: List[dict] = []
        self._training_scores: List[List[dict]] = []
        self._testing_scores: List[List[dict]] = []
        self._ground_truth: Union[None, Set[Gene]] = None

    def train(self) -> None:
        if len(self._scores) > 0:
            if self._training:
                self._training_scores.append(self._scores)
            else:
                self._testing_scores.append(self._scores)
            self._scores = []
        self._training = True

    def test(self) -> None:
        if len(self._scores) > 0:
            if self._training:
                self._training_scores.append(self._scores)
            else:
                self._testing_scores.append(self._scores)
            self._scores = []
        self._training = False

    def reset_ground_truth(self) -> None:
        self._ground_truth = None

    def score(self, heldout_genes: Iterable[Gene],
              predictions: Union[Iterable[Gene],
                                 Iterable[Tuple[Gene, float]]]) -> None:
        """

        Raises:
            Exception: If the requested score type does not exist
        """

        if self._ground_truth is None:
            self._ground_truth = set(map(lambda x: x.name, heldout_genes))

        if self._score_type is ScoreTypes.TOP_K:
            '''
                If the user passes in a list of tuples ensure we
                sort it by score, otherwise we assume it is passed
                in sorted order
            '''
            if all(isinstance(v, tuple) for v in predictions):
                # need to do this for type checking :/
                new_predictions: List[Tuple[Gene, float]
                                      ] = list(predictions)  # type: ignore
                sorted_predictions = sorted(
                    new_predictions,
                    key=lambda x: x[1],
                    reverse=True)  # type: ignore
                predictions = list(
                    map(lambda x: x[0], sorted_predictions))

            predictions = predictions[0:self._k]
            genes_in_ground_truth = list(filter(
                lambda x: x.name in self._ground_truth, predictions))

            self._scores.append({"top_k_predictions": genes_in_ground_truth,
                                 "score": len(genes_in_ground_truth)
                                 / len(self._ground_truth),
                                 "ground_truth": self._ground_truth,
                                 "predictions": predictions})
            return
        else:
            raise Exception(
                f"{self._score_type} is not a valid score function")

    def training_summary(self) -> str:
        if self._training and self._scores:
            self._training_scores.append(self._scores)
            self._scores = []

    def testing_summary(self) -> dict:
        """
            Raises:
                ZeroDivisionError: ...
        """
        # If we are in testing and have scores left
        # ensure that we include them.
        self._collate_testing_scores()

        merged_scores = list(
            itertools.chain.from_iterable(self._testing_scores))
        scores = list(map(lambda x: x['score'], merged_scores))

        predicted_genes = list(
            map(lambda x: (x['ground_truth'], x['predictions']),
                merged_scores))

        return {"k": self._k, "score": scores,
                "avg_score": sum(scores) / len(scores),
                "predicted_genes": predicted_genes}

    def _collate_testing_scores(self) -> None:
        if not self._training and self._scores:
            self._testing_scores.append(self._scores)
            self._scores = []
