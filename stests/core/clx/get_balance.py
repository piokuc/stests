from stests.core.clx.utils import get_client
from stests.core.domain import Account
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import Node
from stests.core.utils import factory
from stests.core.utils import logger


# Default transaction fee to apply.
TX_FEE = 10000000

# Default gas price to apply.
TX_GAS_PRICE = 1


def execute(node: Node, account: Account) -> int:
    """Queries a node for an account balance.

    :param node: Node to which query will be dispatched.
    :param account: Account whose balance will be queried.
    :returns: Account balance.

    """
    client = get_client(node)
    try:
        balance = client.balance(
            address=account.public_key,
            block_hash=get_last_block_hash(client)
            )
    except Exception as err:
        if "Value not found: \" Key::Account" in err.details:
            return 0
        raise err
    else:
        return balance


def get_last_block_hash(client):
    """Returns last blck hash by querying a node.
    
    """
    last_block_info = next(client.showBlocks(1))

    return last_block_info.summary.block_hash.hex()
