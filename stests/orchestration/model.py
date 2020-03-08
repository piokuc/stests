import typing

from stests.core.domain import RunContext
from stests.generators.meta import GENERATOR_MAP as MODULES



class WorkflowStep():
    """A step with a phase of a broader workflow.
    
    """
    def __init__(self, ctx: RunContext, index: int, module):
        """Constructor.
        
        """
        # Workflow execution context information.
        self.ctx = ctx

        # Index within the set of phase steps.
        self.index = index

        # Flag indicating whether this is the last step within the phase.
        self.is_last = False

        # Python module in which the step is declared.
        self.module = module

        # Execution error.
        self.error = None

        # Execution result.
        self.result = None

    @property
    def description(self):
        return self.module.DESCRIPTION

    @property
    def label(self):
        return self.module.LABEL
    
    @property
    def is_async(self):     
        """Is this effectively an asynchronous step - i.e. relies upon chain events to complete."""   
        return hasattr(self.module, "verify_deploy")   


    def execute(self):
        """Performs step execution.
        
        """
        try:
            self.result = self.module.execute(self.ctx)
        except Exception as err:
            self.error = err


class WorkflowPhase():
    """A phase within a broader workflow.
    
    """
    def __init__(self, ctx: RunContext, index: int, module):
        """Constructor.
        
        """
        # Workflow execution context information.
        self.ctx = ctx

        # Index within the set of phases.
        self.index = index

        # Flag indicating whether this is the last phase within the workflow.
        self.is_last = False

        # Python module in which the phase is declared.
        self.module = module

        # Associated steps.
        self.steps = [WorkflowStep(ctx, i, s) for i, s in enumerate(module.STEPS)]
        if self.steps:
            self.steps[-1].is_last = True


    def get_step(self, step_index: int) -> WorkflowStep:
        """Returns a step within managed collection.
        
        """
        return self.steps[step_index - 1]


class Workflow():
    """A workflow executed in order to test a scenario.
    
    """
    def __init__(self, ctx: RunContext, module):
        """Constructor.
        
        """
        # Workflow execution context information.
        self.ctx = ctx

        # Python module in which the workflow is declared.
        self.module = module

        # Associated phases.
        self.phases = [WorkflowPhase(ctx, i, p) for i, p in enumerate(module.PHASES)]
        if self.phases:
            self.phases[-1].is_last = True


    @property
    def description(self):
        return self.module.DESCRIPTION

    @property
    def typeof(self):
        return self.module.TYPE

    
    def get_phase(self, phase_index: int) -> WorkflowPhase:
        """Returns a phase within managed collection.
        
        """
        return self.phases[phase_index - 1]


    def get_step(self, phase_index: int, step_index: int) -> WorkflowStep:
        """Returns a step within managed collection.
        
        """
        phase = self.get_phase(phase_index) 

        return phase.get_step(step_index)


    @staticmethod
    def create(ctx: RunContext):
        """Simple factory method.
        
        :param ctx: Workflow execution context information.

        :returns: Workflow wrapper instance.

        """
        try:
            MODULES[ctx.run_type]
        except KeyError:
            raise ValueError(f"Unsupported workflow type: {ctx.run_type}")
        else:
            return Workflow(ctx, MODULES[ctx.run_type])


    @staticmethod
    def get_phase_(ctx: RunContext, phase_index: int) -> WorkflowPhase:
        """Simple factory method.
        
        :param ctx: Workflow execution context information.

        :returns: Workflow wrapper instance.

        """
        wflow = Workflow.create(ctx)

        return wflow.get_phase(phase_index)


    @staticmethod
    def get_phase_step(ctx: RunContext, phase_index: int, step_index: int) -> WorkflowStep:
        """Simple factory method.
        
        :param ctx: Workflow execution context information.

        :returns: Workflow wrapper instance.

        """
        wflow = Workflow.create(ctx)

        return wflow.get_step(phase_index, step_index)