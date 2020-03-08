import typing
from dataclasses import dataclass

from stests.core.utils.domain import *
from stests.core.domain.enums import ExecutionStatus



@dataclass
class ExecutionRunInfo(Entity):
    """Contextual information associated with each generator run.
    
    """
    # Associated run arguments.
    args: typing.Optional[typing.Any]

    # Number of times to loop.
    loop_count: int

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

    # Index to disambiguate a step within the context of a phase.
    step_index: int

    # Label to disambiguate a step within the context of a phase.
    step_label: typing.Optional[str]

    # Current step.
    # TODO: remove
    run_step: typing.Optional[str]

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


@dataclass
class ExecutionRunLock:
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


@dataclass
class ExecutionRunState(Entity):
    """Execution state information - run.
    
    """
    # Associated network.
    network: str

    # Numerical index to distinguish between multiple runs.
    run_index: int

    # Type of run, e.g. WG-100 ...etc.
    run_type: str

    # Execution status.
    status: ExecutionStatus

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()

    @property
    def run_index_label(self):
        return f"R-{str(self.run_index).zfill(3)}"