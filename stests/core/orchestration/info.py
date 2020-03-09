import dataclasses
import typing
from datetime import datetime

from stests.core.orchestration.enums import ExecutionStatus



@dataclasses.dataclass
class ExecutionInfo:
    """Execution information.
    
    """
    # Associated network.
    network: str

    # Index to disambiguate a phase within the context of a run.
    phase_index: int

    # Numerical index to distinguish between multiple runs.
    run_index: int

    # Type of run, e.g. WG-100 ...etc.
    run_type: str

    # Current status.
    status: ExecutionStatus

    # Index to disambiguate a step within the context of a phase.
    step_index: int

    # Label to disambiguate a step within the context of a phase.
    step_label: str

    # Timeperiod: run duration (in seconds).
    tp_duration: typing.Optional[float]

    # Timestamp: run start.
    ts_start: datetime

    # Timestamp: run end.
    ts_end: typing.Optional[datetime]

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str]

    @property
    def step_index_label(self):
        return f"S-{str(self.step_index).zfill(2)}"

    @property
    def tp_elapsed(self):
        if self.status == ExecutionStatus.COMPLETE:
            return self.tp_duration
        return datetime.now().timestamp() - self.ts_start.timestamp()

    @property
    def tp_duration_label(self):
        """Returns step duration formatted for display purposes.
        
        """
        if self.tp_duration is None:
            return "N/A"

        duration = str(self.tp_duration)
        minutes = duration.split(".")[0]
        seconds = duration.split(".")[1][:6]
        
        return f"{minutes}.{seconds}"

    @property
    def tp_elapsed_label(self):
        """Returns step elapsed formatted for display purposes.
        
        """
        elapsed = str(self.tp_elapsed)
        minutes = elapsed.split(".")[0]
        seconds = elapsed.split(".")[1][:6]
        
        return f"{minutes}.{seconds}"

    @property
    def phase_index_label(self):
        return f"P-{str(self.phase_index).zfill(2)}"

    @property
    def run_index_label(self):
        return f"R-{str(self.run_index).zfill(3)}"


    def end(self, status, error=None):
        """Invoked when execution is complete.
        
        """
        self.error = error
        self.status = status
        self.ts_end = datetime.now()
        self.tp_duration = self.ts_end.timestamp() - self.ts_start.timestamp()
