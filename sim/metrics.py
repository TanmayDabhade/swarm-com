import numpy as np

def coverage_percent(world) -> float:
    free = (world.obstacles == 0)
    if free.sum() == 0:
        return 0.0
    covered = (world.coverage >= 1.0) & free
    return float(covered.sum() / free.sum()) * 100.0
