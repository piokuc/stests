import dramatiq

from stests.core import cache
from stests.core import clx
from stests.core.utils import factory
from stests.core.domain import BlockStatus
from stests.core.domain import Deploy
from stests.core.domain import DeployStatus
from stests.core.domain import NetworkIdentifier
from stests.core.domain import Transfer
from stests.core.domain import TransferStatus
from stests.core.utils import logger
from stests.monitoring.correlator import correlate_finalized_deploy



# Queue to which messages will be dispatched.
_QUEUE = "monitoring"


@dramatiq.actor(queue_name=_QUEUE)
def do_monitor_blocks(network_id: NetworkIdentifier):   
    """Wires upto chain event streaming.
    
    """
    clx.stream_events(
        network_id,
        on_block_finalized=lambda block_hash: on_finalized_block.send(network_id, block_hash)
        )


@dramatiq.actor(queue_name=_QUEUE)
def on_finalized_block(network_id: NetworkIdentifier, block_hash: str):   
    """Event: raised whenever a block is finalized.

    :param network_id: Identifier of network upon which a block has been finalized.
    :param block_hash: Hash of finalized block.

    """
    # Query block info & set block status accordingly.
    block = clx.get_block(network_id, block_hash)
    block.status = BlockStatus.FINALIZED

    # Encache - skip duplicates.
    _, encached = cache.set_network_block(block)  
    if not encached:
        return

    # Enqueue finalized deploys.
    for deploy_hash in clx.get_block_deploys(network_id, block_hash):  
        on_finalized_deploy.send(network_id, block_hash, deploy_hash, block.timestamp)


@dramatiq.actor(queue_name=_QUEUE)
def on_finalized_deploy(network_id: NetworkIdentifier, block_hash: str, deploy_hash: str, ts_finalized: int):   
    """Event: raised whenever a deploy is finalized.
    
    :param network_id: Identifier of network upon which a block has been finalized.
    :param block_hash: Hash of finalized block.
    :param deploy_hash: Hash of finalized deploy.
    :param ts_finalized: Moment in time when finalization occurred.

    """
    # Set network deploy.
    deploy = factory.create_deploy(network_id, block_hash, deploy_hash, DeployStatus.FINALIZED)    

    # Encache - skip duplicates.
    _, encached = cache.set_network_deploy(deploy)
    if not encached:
        return

    # Update run deploy.
    deploy = cache.get_run_deploy(deploy_hash)
    if not deploy:
        logger.log_warning(f"Could not find finalized run deploy information: {block_hash} : {deploy_hash}")
        return
    deploy.block_hash = block_hash
    deploy.status = DeployStatus.FINALIZED
    deploy.ts_finalized = ts_finalized
    cache.set_run_deploy(deploy)

    # Update run step deploy.
    ctx = cache.get_run_context(deploy.network, deploy.run, deploy.run_type)
    cache.set_run_step_deploy(ctx, deploy)

    # Update transfer.
    transfer = cache.get_run_transfer(deploy_hash)
    if transfer:
        transfer.status = TransferStatus.COMPLETE
        cache.set_run_transfer(transfer)
    
    # Signal downstream to workload generator.
    correlate_finalized_deploy.send(ctx, deploy_hash)
