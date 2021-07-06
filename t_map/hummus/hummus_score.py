from typing import Union, List, Tuple, Callable, Iterable, Set
from t_map.gene.gene import Gene

ScoreFn = Callable[[Union[List[Gene], List[Tuple[Gene, float]]]], None]


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

    def score(self, heldout_genes: Iterable[Gene],
              predictions: Union[List[Gene],
                                 List[Tuple[Gene, float]]]) -> None:
        """

        Raises:
            Exception: If the requested score type does not exist
        """

        if self._ground_truth is None:
            self._ground_truth = set(heldout_genes)

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
            genes_in_ground_truth = list(filter(
                lambda x: x in self._ground_truth, predictions))

            self._scores.append({"top_k_predictions": genes_in_ground_truth,
                                 "score": len(genes_in_ground_truth) / self._k,
                                 "predictions": predictions})
            return
        else:
            raise Exception(
                f"{self._score_type} is not a valid score function")

    def training_summary(self) -> str:
        if self._training and self._scores:
            self._training_scores.append(self._scores)
            self._scores = []

    def testing_summary(self) -> str:
        # If we are in testing and have scores left
        # ensure that we include them.
        if not self._training and self._scores:
            self._testing_scores.append(self._scores)
            self._scores = []

        scores = list(map(lambda x: x['score'], self._scores))

        return (f"For k={self._k}, the scores we got were:\n",
                f"{scores}\n",
                f"Averaging out to f{sum(scores) / len(scores)}")
