from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Sequence, Tuple

from .state import QuantumState
from .history import History, OperationRecord


RandomSource = Callable[[], float]


@dataclass(frozen=True)
class MeasurementOutcome:
    index: int
    probability: float
    post_state: QuantumState


def _sample_from_probabilities(
    probabilities: Sequence[float], rng: RandomSource | None = None
) -> int:
    if rng is None:
        rng = random.random
    total = sum(probabilities)
    if total <= 0:
        raise ValueError("Probabilities must have positive sum.")
    # Normalise just in case of rounding.
    probs = [p / total for p in probabilities]
    r = rng()
    acc = 0.0
    for i, p in enumerate(probs):
        acc += p
        if r <= acc:
            return i
    return len(probs) - 1


def measure_in_computational_basis(
    state: QuantumState,
    history: History | None = None,
    rng: RandomSource | None = None,
) -> MeasurementOutcome:
    """
    Perform a projective measurement in the computational basis.

    Returns the index obtained, its probability, and the post-measurement
    collapsed state. If a `History` is provided, the measurement is recorded.
    """
    probabilities = [state.probability_of_basis_state(i) for i in range(state.dimension)]
    index = _sample_from_probabilities(probabilities, rng=rng)
    probability = probabilities[index]

    # Post-measurement state is |i⟩; for a single qubit this is either |0⟩ or |1⟩.
    amplitudes = tuple(1 + 0j if i == index else 0 + 0j for i in range(state.dimension))
    post_state = QuantumState(amplitudes)

    if history is not None:
        history.record(
            OperationRecord(
                timestamp=datetime.now(timezone.utc),
                description=f"measure computational basis → outcome {index}",
                pre_state=state,
                post_state=post_state,
            )
        )

    return MeasurementOutcome(index=index, probability=probability, post_state=post_state)

