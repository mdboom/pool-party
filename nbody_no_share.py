from nbody import *


def bench(loops, reference=DEFAULT_REFERENCE, iterations=DEFAULT_ITERATIONS):
    bodies = copy.deepcopy(BODIES)
    system = copy.deepcopy(SYSTEM)
    pairs = copy.deepcopy(PAIRS)

    # Set up global state
    offset_momentum(bodies[reference], system)

    range_it = range(loops)

    result = []

    for x in range_it:
        advance(0.01, iterations, system, pairs)
        result.append(report_energy(system, pairs))

    return result
