from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Sequence

from .state import QuantumState


@dataclass(frozen=True)
class OperationRecord:
    timestamp: datetime
    description: str
    pre_state: QuantumState
    post_state: QuantumState


class History:
    """
    Immutable-style append-only history of quantum operations.

    Conceptually, this is a \"time register\" used to reason about what it means
    to reconstruct a prior state of uncertainty.
    """

    def __init__(self, records: Sequence[OperationRecord] | None = None) -> None:
        self._records: List[OperationRecord] = list(records) if records else []

    @property
    def records(self) -> Sequence[OperationRecord]:
        return tuple(self._records)

    def record(self, op: OperationRecord) -> None:
        self._records.append(op)

    def last_state(self) -> QuantumState | None:
        if not self._records:
            return None
        return self._records[-1].post_state

    def state_at(self, index: int) -> QuantumState:
        return self._records[index].post_state

