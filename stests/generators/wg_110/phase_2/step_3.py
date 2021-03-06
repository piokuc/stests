from stests.core.orchestration import ExecutionContext
from stests.core.utils import logger



# Step description.
DESCRIPTION = "Dispatches a notification to signal that generator has completed."

# Step label.
LABEL = "notify-completion"


def execute(ctx: ExecutionContext):
    """Step entry point.
    
    :param ctx: Execution context information.

    """      
    # TODO: push notification.
    pass


def verify(ctx: ExecutionContext):
    """Step verifier.
    
    :param ctx: Execution context information.

    """
    # TODO: verify notification was pushed
    return True
