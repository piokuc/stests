import abc
import uuid
import dataclasses
from datetime import datetime



def get_timestamp_field() -> dataclasses.field:
    """Returns a timestamp field.
    
    :returns: Dataclass field.

    """
    return dataclasses.field(
        default_factory=lambda: datetime.now(),
    )


def get_uuid_field() -> dataclasses.field:
    """Returns a UUID4 field.
    
    :returns: Dataclass field.

    """
    return dataclasses.field(
        default_factory=lambda: str(uuid.uuid4()),
    )
