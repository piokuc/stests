import redis

from stests.core.cache.enums import StorePartition
from stests.core.utils import env



# Environment variables required by this module.
class EnvVars:
    # Redis host.
    DB = env.get_var('CACHE_REDIS_DB', 1, int)

    # Redis host.
    HOST = env.get_var('CACHE_REDIS_HOST', "localhost")

    # Redis port.
    PORT = env.get_var('CACHE_REDIS_PORT', 6379, int)


# Map: partition type -> cache db index offset.
PARTITION_OFFSETS = {
    StorePartition.INFRA: 0,
    StorePartition.MONITORING: 1,
    StorePartition.ORCHESTRATION: 2,
    StorePartition.STATE: 3,
}


def get_store(partition_type: StorePartition) -> redis.Redis:
    """Returns instance of a redis cache store accessor.

    :returns: An instance of a redis cache store accessor.

    """
    # Set cache db index.
    db = EnvVars.DB
    db += PARTITION_OFFSETS[partition_type]

    # TODO: 1. cluster connections
    return redis.Redis(
        db=db,
        host=EnvVars.HOST,
        port=EnvVars.PORT
        )

