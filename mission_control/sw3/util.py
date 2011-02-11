
import pid
from mixer import mixer

def pairwise_disjoint(*args):
    for i in range(0, len(args) - 1):
        for e in args[i+1:]:
            if not e.isdisjoint(args[i]):
                return False
    return True

def add_angle(a, b):
    return (((a + 180) + b) % 360) - 180
