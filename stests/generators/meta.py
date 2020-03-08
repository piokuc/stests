import stests.generators.wg_100.meta as wg_100



# Set of generators.
GENERATOR_SET = {
    wg_100,
}

# Map: generator type --> generator module.
GENERATOR_MAP = {i.TYPE:i for i in GENERATOR_SET}