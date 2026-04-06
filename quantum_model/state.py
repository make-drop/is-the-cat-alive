from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import cmath


def _normalize(state: Sequence[complex]) -> tuple[complex, ...]:
    norm_sq = sum(abs(a) ** 2 for a in state)
    if norm_sq == 0:
        raise ValueError("State vector cannot be the zero vector.")
    factor = 1.0 / norm_sq**0.5
    return tuple(a * factor for a in state)


@dataclass(frozen=True)
class QuantumState:
    """
    Minimal representation of a pure quantum state |ψ⟩ in a finite-dimensional
    Hilbert space.

    For the current project we focus on a single qubit, so `amplitudes`
    is a 2-component vector (α, β) in the computational basis {|0⟩, |1⟩}.
    """

    amplitudes: tuple[complex, ...]

    def __post_init__(self) -> None:
        # Enforce normalisation and immutability at construction.
        object.__setattr__(self, "amplitudes", _normalize(self.amplitudes))

    @classmethod
    def basis_zero(cls) -> "QuantumState":
        """Convenience constructor for |0⟩."""
        return cls((1 + 0j, 0 + 0j))

    @classmethod
    def basis_one(cls) -> "QuantumState":
        """Convenience constructor for |1⟩."""
        return cls((0 + 0j, 1 + 0j))

    @property
    def dimension(self) -> int:
        return len(self.amplitudes)

    def apply(self, operator: Sequence[Sequence[complex]]) -> "QuantumState":
        """
        Apply a linear operator U to this state, returning the new state U|ψ⟩.

        The caller is responsible for ensuring that `operator` is unitary if
        they want to model physical evolution.
        """
        dim = self.dimension
        if len(operator) != dim or any(len(row) != dim for row in operator):
            raise ValueError("Operator dimensions do not match state dimension.")

        result: list[complex] = []
        for row in operator:
            acc = 0 + 0j
            for a, u in zip(self.amplitudes, row):
                acc += u * a
            result.append(acc)

        return QuantumState(tuple(result))

    def probability_of_basis_state(self, index: int) -> float:
        """Return the Born-rule probability of obtaining a given basis index."""
        if not (0 <= index < self.dimension):
            raise IndexError("Basis index out of range.")
        amp = self.amplitudes[index]
        return abs(amp) ** 2

    def is_in_superposition(self, tolerance: float = 1e-9) -> bool:
        """
        Heuristic notion of "superposition" in the computational basis:
        at least two components have non-negligible probability.
        """
        non_negligible = [
            i for i, a in enumerate(self.amplitudes) if abs(a) ** 2 > tolerance
        ]
        return len(non_negligible) > 1

