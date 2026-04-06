# Quantum \"Is The Cat Alive\" Simulator

This project models, in a simplified and educational way, the idea that in
quantum mechanics one can **reconstruct a past state of uncertainty** if – and
only if – one can **recreate the conditions that generated that uncertainty**.

In the language of Schrödinger's cat:

- Once you open the box and observe the cat, the state collapses (the cat is
  either alive or dead).
- It is **not** possible to \"un-observe\" that specific cat.
- But you can prepare a **new cat** in the **same superposed quantum state**
  as before: the *uncertainty* is regenerated, even if the individual system
  is different.

This repository contains:

- A small **quantum model library** (`quantum_model/`) with a formal
  representation of a single-qubit state, unitary operations, measurement, and
  a history/\"time\" abstraction.
- A **CLI educational simulator** (`cli/main.py`) that guides the user through
  Schrödinger's cat and the regeneration of uncertainty.

## Installation

The core implementation uses only the Python standard library. To run the CLI
experiment, install the package in a virtual environment (optional but
recommended) and install test tools if desired:

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\\Scripts\\activate
pip install -e .
pip install pytest
```

Alternatively you can simply run the files with the system Python without
installing as a package.

## Running the simulator

From the repository root:

```bash
python -m cli.main
```

You will be guided through:

1. **Schrödinger's cat experiment** – preparation in |0⟩, application of
   the Hadamard gate (superposition), and measurement.
2. **Regeneration of uncertainty** – demonstration of two conceptual modes:
   - *Unitary inversion* (idealised, purely mathematical reconstruction of
     a past quantum state).
   - *Re-preparation* of a new system with the same superposition as the
     original cat-before-measurement.

## Conceptual model

- States are represented as vectors \\( |ψ\\rangle = (α, β) \\) in a
  2-dimensional Hilbert space (single qubit) in the computational basis
  \\(|0\\rangle, |1\\rangle\\). Vectors are automatically normalised.
- Unitary operations (e.g. Hadamard, Pauli-X) are 2×2 complex matrices acting
  on the state by left-multiplication.
- Measurement in the computational basis uses the Born rule: the probability
  of outcome *i* is \\(|α_i|^2\\), and the post-measurement state is the
  corresponding basis vector.
- A **History** object records operations and states over (logical) time so
  that we can reason about \"returning\" to a previous state of uncertainty.

### Time, history, and \"returning to the past\"

The function `regenerate_uncertainty` captures the central idea:

- Given a point in the history where the state was in superposition, we can
  either:
  - Model an **ideal unitary inversion**: conceptually apply the inverse of all
    subsequent unitary operations to reconstruct \\(|ψ\\rangle\\).
  - **Re-prepare** a new system in the *same type* of superposition (for
    example, again applying Hadamard to |0⟩).
- In both cases the observable statistics for future measurements can match
  those of the past state of uncertainty, but:
  - No causal paradoxes are introduced.
  - The code and documentation stress that this is a **reconstruction of
    state**, not physical time travel.

## Development and testing

Run tests with:

```bash
pytest
```

The tests validate:

- State normalisation.
- Correct action of the Hadamard gate on |0⟩.
- Measurement behaviour and history recording.
- Regeneration of an uncertainty state via re-preparation.

