from stests.core.domain.account import *
from stests.core.domain.block import *
from stests.core.domain.deploy import *
from stests.core.domain.enums import *
from stests.core.domain.identifiers import *
from stests.core.domain.meta import *
from stests.core.domain.network import *
from stests.core.domain.node import *
from stests.core.domain.run import *
from stests.core.domain.transfer import *



# Set of supported classes.
DCLASS_SET = {
    Account,
    Transfer,
    Block,
    Deploy,
    Network,
    Node,
    Transfer,
    
    RunContext,
    RunEvent,
}

# Set of supported identifiers.
IDENTIFIER_SET = {
    AccountIdentifier,
    NetworkIdentifier,
    NodeIdentifier,
    RunIdentifier
}

MCLASS_SET = {
    TypeMetadata,
    DeployMetadata,
}

# Full domain type set.
TYPE_SET = DCLASS_SET | IDENTIFIER_SET | MCLASS_SET | ENUM_SET

# Register domain types with encoder.
from stests.core.utils import encoder
for i in TYPE_SET:
    encoder.register_type(i)
