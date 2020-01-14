from dataclasses import dataclass
import typing

from dataclasses_json import dataclass_json



class ExecutionServices():
    """Exposes services available to actors.
    
    """
    # Cache store accessor.
    cache: typing.Any


@dataclass_json
@dataclass
class ExecutionContext():
    """Encpasulates information & services relevant to current execution context.
    
    """
    # Identifier of network being tested.
    network_id: str

    # Type of simulation being executed.
    simulation_type: str

    # Identifier of simulation being executed.
    simulation_id: int = 0

    # Note: not serialised.
    services: typing.ClassVar[ExecutionServices] = ExecutionServices()


    @staticmethod
    def create(
        network_id: str,
        simulation_type: str,
        simulation_id: int = 0        
        ):
        """Returns an instance ready for use within a workflow.

        :param network_id: Identifier of network being tested.
        :param simulation_type: Type of simulation being run.
        :param simulation_id: Identifier of current run.
        :returns: An execution context instance ready for use by actors.

        """        
        # JIT import to avoid circular references.
        from stests.core import cache

        # Instantiate.
        ctx = ExecutionContext(network_id, simulation_type, simulation_id)

        # Set actor services.
        ctx.services.cache = cache.get_store(ctx) 

        return ctx
