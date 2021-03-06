import dataclasses
import typing
from datetime import datetime

from stests.core.domain.enums import ClientContractType
from stests.core.utils.dataclasses import get_timestamp_field



@dataclasses.dataclass
class ClientContract:
    """A test network.
    
    """
    # Hash key that points to the stored contract.
    chash: str

    # Associated network.
    network: typing.Optional[str]
    
    # Type of client contract.
    typeof: ClientContractType

    # Type key of associated object used in serialisation scenarios.
    _type_key: typing.Optional[str] = None

    # Timestamp: create.
    _ts_created: datetime = get_timestamp_field()

