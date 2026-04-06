from datetime import datetime

from quantum_model import (
    History,
    OperationRecord,
    QuantumState,
    hadamard,
    measure_in_computational_basis,
    regenerate_uncertainty,
)


def test_quantum_state_normalization():
    s = QuantumState((2 + 0j, 0 + 0j))
    assert abs(abs(s.amplitudes[0]) ** 2 + abs(s.amplitudes[1]) ** 2 - 1.0) < 1e-9


def test_hadamard_superposition():
    s0 = QuantumState.basis_zero()
    h = hadamard()
    s = s0.apply(h)
    # For ideal H|0>, probabilities are 1/2, 1/2.
    p0 = s.probability_of_basis_state(0)
    p1 = s.probability_of_basis_state(1)
    assert abs(p0 - 0.5) < 1e-9
    assert abs(p1 - 0.5) < 1e-9
    assert s.is_in_superposition()


def test_measurement_collapses_state_with_correct_probabilities():
    s0 = QuantumState.basis_zero().apply(hadamard())
    history = History()

    # Use deterministic RNG that always selects the lowest index.
    def zero_rng():
        return 0.0

    outcome = measure_in_computational_basis(s0, history=history, rng=zero_rng)
    assert outcome.index == 0
    assert outcome.post_state.probability_of_basis_state(0) == 1.0
    assert len(history.records) == 1


def test_regenerate_uncertainty_reprepare_returns_superposition():
    s0 = QuantumState.basis_zero()
    s_super = s0.apply(hadamard())
    history = History()
    history.record(
        OperationRecord(
            timestamp=datetime.utcnow(),
            description="prepare superposition",
            pre_state=s0,
            post_state=s_super,
        )
    )

    result = regenerate_uncertainty(history, strategy="reprepare")
    assert result.new_state.is_in_superposition()

