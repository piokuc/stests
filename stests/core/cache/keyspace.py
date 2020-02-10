from stests.core.domain import Account
from stests.core.domain import AccountType
from stests.core.domain import Network
from stests.core.domain import NetworkIdentifier
from stests.core.domain import Node
from stests.core.domain import NodeIdentifier
from stests.core.domain import RunContext
from stests.core.domain import RunEvent



def get_key(obj):
    """Returns key derived from a domain type instance.
    
    """
    if isinstance(obj, Account):
        zfill = 6 if obj.typeof == AccountType.USER else 2
        return f"accounts:{obj.typeof.name}:{str(obj.index).zfill(zfill)}"

    if isinstance(obj, (Network, NetworkIdentifier)):
        return obj.name

    if isinstance(obj, NodeIdentifier):
        key = get_key(obj.network)
        return f"{key}.NODE:{str(obj.index).zfill(4)}"

    if isinstance(obj, Node):
        return f"{obj.network}.NODE:{str(obj.index).zfill(4)}"

    if isinstance(obj, RunContext):
        return f"{obj.network}.{obj.typeof}:R-{str(obj.index).zfill(3)}"

    if isinstance(obj, RunEvent):
        return f"events:{obj.timestamp}.{obj.event}"