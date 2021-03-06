import dataclasses



@dataclasses.dataclass
class RunLock:
    """Execution lock information - run.
    
    """
    # Associated network.
    network: str

    # Numerical index to distinguish between multiple runs of the same workflow.
    run_index: int

    # Type of workflow, e.g. WG-100 ...etc.
    run_type: str

    @property
    def run_index_label(self):
        return f"R-{str(self.run_index).zfill(3)}"


@dataclasses.dataclass
class PhaseLock(RunLock):
    """Execution lock information - phase.
    
    """
    # Numerical index to distinguish between multiple phases within a run.
    phase_index: int

    @property
    def phase_index_label(self):
        return f"P-{str(self.phase_index).zfill(2)}"


@dataclasses.dataclass
class StepLock(PhaseLock):
    """Execution lock information - step.
    
    """
    # Numerical index to distinguish between multiple steps within a phase.
    step_index: int

    @property
    def step_index_label(self):
        return f"S-{str(self.step_index).zfill(2)}"


@dataclasses.dataclass
class StreamLock:
    """Execution lock information - stream.
    
    """
    # Associated network.
    network: str

    # Numerical index to distinguish between nodees upon the same network.
    node_index: int

    # Numerical index to distinguish between multiple locks.
    lock_index: int
