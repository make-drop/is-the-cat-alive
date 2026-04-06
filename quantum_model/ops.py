from __future__ import annotations

import math
from typing import Tuple


Matrix2x2 = Tuple[Tuple[complex, complex], Tuple[complex, complex]]


def hadamard() -> Matrix2x2:
    """
    Hadamard gate for a single qubit.

    H = (1/√2) [[1,  1],
                [1, -1]]
    """
    inv_sqrt2 = 1.0 / math.sqrt(2.0)
    return (
        (inv_sqrt2 + 0j, inv_sqrt2 + 0j),
        (inv_sqrt2 + 0j, -inv_sqrt2 + 0j),
    )


def pauli_x() -> Matrix2x2:
    """
    Pauli-X gate (quantum NOT) for a single qubit.

    X = [[0, 1],
         [1, 0]]
    """
    return (
        (0 + 0j, 1 + 0j),
        (1 + 0j, 0 + 0j),
    )

