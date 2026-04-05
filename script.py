import random
import time
import sys


class SimulatedQubit:
    """
    Simulates a Qubit (Quantum Bit).
    Unlike a classical bit (0 or 1), this object can exist
    in a state of 'superposition' until measured.
    """

    def __init__(self, name="Qubit"):
        self.name = name
        self.measured_state = None  # None represents undefined state
        self.in_superposition = False

    def apply_hadamard(self):
        """
        The Hadamard gate (H-gate) creates superposition.
        It's equivalent to putting the Cat in the box.
        """
        self.in_superposition = True
        self.measured_state = None
        print(f"[{self.name}] entered SUPERPOSITION. (|0> + |1>)")
        print(f"   Now it is simultaneously 0 and 1 (or Alive and Dead).")

    def measure(self):
        """
        The act of observing collapses the wave function.
        This is the 'Quantum Leap' from a state of possibility to a defined reality.
        """
        if not self.in_superposition and self.measured_state is not None:
            return self.measured_state

        print(f"Observing {self.name}...")
        time.sleep(1)  # Suspense...

        # Wave function collapse (50% probability)
        self.measured_state = random.choice([0, 1])
        self.in_superposition = False

        state_str = "|1> (ON/ALIVE)" if self.measured_state == 1 else "|0> (OFF/DEAD)"
        print(f"QUANTUM LEAP OCCURRED! State collapsed into: {state_str}")
        return self.measured_state

    def regenerate_uncertainty(self):
        """
        Restores the qubit to a state of superposition (uncertainty).
        Equivalent to applying the Hadamard gate again after measurement:
        the outcome becomes unknown, as if the qubit was never observed.
        """
        self.in_superposition = True
        self.measured_state = None
        print(f"[{self.name}] uncertainty regenerated → back to superposition (|0> + |1>)")
        print(f"   The cat is once again both Alive and Dead.")

def main():
    print("=== QUANTUM CONCEPTS SIMULATOR ===")

    # Schrödinger's Cat
    print("\n1. EXPERIMENT: SCHRODINGER'S CAT (Superposition)")
    cat = SimulatedQubit("Cat")
    cat.apply_hadamard()  # Put the cat in the box

    input("Press ENTER to open the box (measure)...")
    cat.measure()

    # Regenerate Uncertainty
    print("\n2. EXPERIMENT: REGENERATE UNCERTAINTY (Reset)")
    # It doesn't matter if the cat is alive or dead, we reset it
    time.sleep(0.5)
    cat.regenerate_uncertainty()

    print("\n=== END OF SIMULATION ===")


if __name__ == "__main__":
    main()