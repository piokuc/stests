import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.domain import DeployStatus
from stests.core.orchestration import ExecutionContext
from stests.core.orchestration import ExecutionAspect
from stests.core.domain import Transfer
from stests.core.domain import TransferStatus
from stests.generators.wg_100 import constants


# Queue to which messages will be dispatched.
_QUEUE = "wg-100.utils"


@dramatiq.actor(queue_name=_QUEUE)
def do_refund(ctx: ExecutionContext, cp1_index: int, cp2_index: int):
    """Performs a refund ot funds between 2 counterparties.

    :param ctx: Execution context information.
    :param cp1_index: Run specific account index of counter-party one.
    :param cp2_index: Run specific account index of counter-party two.
    
    """
    # Pull accounts.
    cp1 = cache.state.get_account_by_run(ctx, cp1_index)
    if cp2_index == constants.ACC_NETWORK_FAUCET:
        network = cache.orchestration.get_run_network(ctx)
        if not network.faucet:
            raise ValueError("Network faucet account does not exist.")
        cp2 = network.faucet
    else:
        cp2 = cache.state.get_account_by_run(ctx, cp2_index)

    # Refund CLX from cp1 -> cp2.
    (deploy, refund) = clx.do_refund(ctx, cp1, cp2)

    # Update cache.
    cache.state.set_run_deploy(deploy)
    cache.state.set_run_transfer(refund)


def verify_deploy(ctx: ExecutionContext, dhash: str):
    """Verifies that a deploy is in a finalized state.
    
    """
    deploy = cache.state.get_run_deploy(dhash)
    assert deploy
    assert deploy.status == DeployStatus.FINALIZED


def verify_deploy_count(ctx: ExecutionContext, expected: int):
    """Verifies that a step's count of finalized deploys tallies.
    
    """
    assert cache.orchestration.get_deploy_count(ctx, ExecutionAspect.STEP) == expected


def verify_refund(ctx: ExecutionContext, dhash: str) -> Transfer:
    """Verifies that a refund between counter-parties completed.
    
    """
    refund = cache.state.get_run_transfer(dhash)
    assert refund
    assert refund.status == TransferStatus.COMPLETE