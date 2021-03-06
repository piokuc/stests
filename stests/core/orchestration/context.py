import dataclasses
import typing
from datetime import datetime

from stests.core.orchestration.enums import ExecutionStatus
from stests.core.utils.dataclasses import get_timestamp_field



@dataclasses.dataclass
class ExecutionContext:
    """Execution context information - run.
    
    """
    # Associated run arguments.
    args: typing.Optional[typing.Any]

    # Number of times to loop.
    loop_count: int

    # Numerical index to distinguish between loops.
    loop_index: int

    # Upon successful completion of a run, the number of seconds after which a new run will be started.
    loop_interval: int

    # Associated network.
    network: str

    # Associated node index.
    node_index: int

    # Numerical index to distinguish between multiple runs.
    run_index: int

    # Type of run, e.g. WG-100 ...etc.
    run_type: str

    # Index to disambiguate a phase within the context of a run.
    phase_index: int

    # Current status.
    status: ExecutionStatus

    # Index to disambiguate a step within the context of a phase.
    step_index: int

    # Label to disambiguate a step within the context of a phase.
    step_label: typing.Optional[str]

    # Flag to indicate use of so-called stored contracts, i.e. on chain contracts.
    use_stored_contracts: bool

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()

    @property
    def run_index_label(self):
        return f"R-{str(self.run_index).zfill(3)}"

    @property
    def phase_index_label(self):
        return f"P-{str(self.phase_index).zfill(2)}"        

    @property
    def step_index_label(self):
        return f"S-{str(self.step_index).zfill(2)}"

    @property
    def next_phase_index(self):
        return self.phase_index + 1

    @property
    def next_phase_index_label(self):
        return f"P-{str(self.next_phase_index).zfill(2)}"        

    @property
    def next_step_index(self):
        return self.step_index + 1

    @property
    def next_step_index_label(self):
        return f"S-{str(self.next_step_index).zfill(2)}"
