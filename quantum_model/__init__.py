"""
Core quantum model package.

This package provides a minimal but formal representation of quantum states
and operations suitable for educational simulations such as the
\"Schrödinger's cat\" thought experiment.
"""

from .state import QuantumState
from .ops import hadamard, pauli_x
from .measurement import measure_in_computational_basis
from .history import History, OperationRecord
from .time_reversal import regenerate_uncertainty

__all__ = [
    "QuantumState",
    "hadamard",
    "pauli_x",
    "measure_in_computational_basis",
    "History",
    "OperationRecord",
    "regenerate_uncertainty",
]

