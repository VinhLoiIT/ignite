import editdistance as ed
import torch
from ignite.exceptions import NotComputableError
from ignite.metrics.metric import Metric, reinit__is_reduced, sync_all_reduce

__all__ = [
    "EditDistance",
    "CharacterErrorRate",
    "WordErrorRate",
]


class EditDistance(Metric):
    """
    Calculates the EditDistance.
    - `update` must receive output of the form `(y_pred, y)` or `{'y_pred': y_pred, 'y': y}`.
    """

    def __init__(self, output_transform=lambda x: x, device=None):
        super().__init__(output_transform, device)

    def compute_distance(self, predict: str, target: str) -> float:
        """
        Compute edit distance between two strings
        """
        raise NotImplementedError()

    @reinit__is_reduced
    def reset(self) -> None:
        self._ed = 0.0
        self._num_examples = 0

    @reinit__is_reduced
    def update(self, output) -> None:
        y_pred, y = output
        assert len(y_pred) == len(y)

        batch_size = len(y)

        for predict, target in zip(y_pred, y):
            distance = self.compute_distance(predict, target)
            self._ed += distance

        self._num_examples += batch_size

    @sync_all_reduce("_ed", "_num_examples")
    def compute(self):
        if self._num_examples == 0:
            raise NotComputableError("EditDistance must have at least one example before it can be computed.")
        return self._ed / self._num_examples


class CharacterErrorRate(EditDistance):
    """
    Calculates the CharacterErrorRate.
    - `update` must receive output of the form `(y_pred, y)` or `{'y_pred': y_pred, 'y': y}`.
    """

    def __init__(self, logfile=None, output_transform=lambda x: x, device=None):
        super().__init__(logfile, output_transform, device)

    def compute_distance(self, predict: str, target: str) -> float:
        """
        Compute edit distance between two strings
        """
        distance = ed.distance(predict, target)
        distance = float(distance) / len(target)
        return distance


class WordErrorRate(EditDistance):
    """
    Calculates the WordErrorRate.
    Notes:
    - `update` must receive output of the form `(y_pred, y)` or `{'y_pred': y_pred, 'y': y}`.
    """

    def __init__(self, output_transform=lambda x: x, device=None):
        super().__init__(output_transform, device)

    def compute_distance(self, predict: str, target: str) -> float:
        """
        Compute edit distance between two strings
        """
        predict = "".join(predict).split(" ")
        target = "".join(target).split(" ")
        distance = ed.distance(predict, target)
        distance = float(distance) / len(target)
        return distance
