import random

def evaluate(v):
    if isinstance(v, (int,float)):
        return v
    elif hasattr(v, "x") and hasattr(v, "y"):
        return random.uniform(v.x, v.y)
    elif isinstance(v, (list, tuple)) and len(v) == 2:
        return random.uniform(v[0], v[1])
    else:
        raise Exception()