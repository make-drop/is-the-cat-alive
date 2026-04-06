from __future__ import annotations

import sys
from datetime import datetime, timezone

from quantum_model import (
    History,
    OperationRecord,
    QuantumState,
    hadamard,
    measure_in_computational_basis,
    regenerate_uncertainty,
)


def _prompt(msg: str) -> None:
    input(msg)


def scenario_cat_experiment() -> None:
    print("=== EXPERIMENT: SCHRÖDINGER'S CAT ===")
    history = History()

    # 1. Prepare in |0⟩ (alive by convention).
    state = QuantumState.basis_zero()
    print("We prepare the system in |0> (the cat is definitely alive).")

    # 2. Apply Hadamard → superposition.
    state_after_h = state.apply(hadamard())
    history.record(
        OperationRecord(
            timestamp=datetime.now(timezone.utc),
            description="apply Hadamard (put cat in the box)",
            pre_state=state,
            post_state=state_after_h,
        )
    )
    print("We apply the Hadamard gate: the cat is now in superposition (alive and dead).")

    _prompt("Press ENTER to 'open the box' (measure)...")
    outcome = measure_in_computational_basis(state_after_h, history=history)
    label = "ALIVE (|0>)" if outcome.index == 0 else "DEAD (|1>)"
    print(f"Observation result = {label}, theoretical probability ≈ {outcome.probability:.2f}")

    return history


def scenario_regenerate_uncertainty(history: History) -> None:
    print("\n=== EXPERIMENT: REGENERATE UNCERTAINTY ===")
    print(
        "After observing the cat, the state has collapsed.\n"
        "We cannot 'un-measure' that specific cat, but we can:\n"
        "  (a) Model an ideal unitary inversion (closed-system idealisation), or\n"
        "  (b) Create a NEW system with the same uncertainty (a new cat).\n"
    )

    while True:
        choice = input("Choose [a] ideal inversion, [b] new cat: ").strip().lower()
        if choice in {"a", "b"}:
            break

    if choice == "a":
        result = regenerate_uncertainty(history, strategy="unitary_inversion")
        print(
            "Mode: IDEAL unitary inversion.\n"
            "In this model we assume we can reconstruct the pre-measurement state.\n"
            "This is not physical time travel; it is a mathematical reconstruction."
        )
    else:
        result = regenerate_uncertainty(history, strategy="reprepare")
        print(
            "Mode: NEW CAT.\n"
            "We prepare a new system in superposition again (e.g. H|0>),\n"
            "which restores the same uncertainty as the original pre-measurement cat."
        )

    new_state = result.new_state
    print("\nMeasuring the new state...")
    outcome = measure_in_computational_basis(new_state)
    label = "ALIVE (|0>)" if outcome.index == 0 else "DEAD (|1>)"
    print(f"New experiment result = {label}, theoretical probability ≈ {outcome.probability:.2f}")


def main(argv: list[str] | None = None) -> int:
    print("=== QUANTUM CONCEPTS SIMULATOR ===")
    history = scenario_cat_experiment()
    scenario_regenerate_uncertainty(history)
    print("\n=== END OF SIMULATION ===")
    return 0


if __name__ == "__main__":  # pragma: no cover - entry point
    raise SystemExit(main(sys.argv[1:]))

