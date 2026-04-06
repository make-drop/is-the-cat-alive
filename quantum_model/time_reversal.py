from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .history import History
from .ops import hadamard
from .state import QuantumState


Strategy = Literal["unitary_inversion", "reprepare"]


@dataclass(frozen=True)
class UncertaintyRegenerationResult:
    """
    Describes how uncertainty was regenerated.

    - strategy = \"unitary_inversion\": we (ideally) apply the inverse of a known
      sequence of operations (closed-system idealisation).
    - strategy = \"reprepare\": we prepare a new system in the same target
      superposition (the \"new cat\" interpretation).
    """

    strategy: Strategy
    new_state: QuantumState


def _default_target_index(history: History) -> int:
    """
    Pick a sensible default target for uncertainty regeneration.

    We want the most recent state that is still in superposition, not the last
    recorded state (which is often post-measurement and therefore collapsed).
    """
    for i in range(len(history.records) - 1, -1, -1):
        if history.state_at(i).is_in_superposition():
            return i
    # Fallback: if no superposition state exists in history, use the latest state.
    return len(history.records) - 1


def regenerate_uncertainty(
    history: History,
    target_index: int | None = None,
    strategy: Strategy = "reprepare",
) -> UncertaintyRegenerationResult:
    """
    Regenerate an \"equivalent\" uncertainty state from the recorded history.

    Two explicit modes are supported:
    - \"reprepare\" (default): prepare a new system in the same kind of
      superposition (e.g. H|0⟩). This matches the \"new cat\" interpretation.
    - \"unitary_inversion\": an idealised mode for a closed system where the
      full unitary evolution is known and invertible.
    """
    if target_index is None:
        target_index = _default_target_index(history)

    target_state = history.state_at(target_index)

    if strategy == "unitary_inversion":
        # In a complete model we would build U^{-1}. Here we explicitly keep
        # this as an idealised reconstruction by returning the historical state.
        return UncertaintyRegenerationResult(strategy="unitary_inversion", new_state=target_state)

    # "reprepare" strategy: for a single qubit, use a standard preparation.
    # If the target state is in superposition in the computational basis,
    # prepare H|0⟩; otherwise recreate the most likely basis state.
    if target_state.is_in_superposition():
        state = QuantumState.basis_zero().apply(hadamard())
    else:
        # Classical-like state: choose the most probable basis state in the target.
        probs = [target_state.probability_of_basis_state(i) for i in range(target_state.dimension)]
        best_index = max(range(len(probs)), key=lambda i: probs[i])
        amplitudes = tuple(1 + 0j if i == best_index else 0 + 0j for i in range(len(probs)))
        state = QuantumState(amplitudes)

    return UncertaintyRegenerationResult(strategy="reprepare", new_state=state)

