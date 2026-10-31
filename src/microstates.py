import time
import tracemalloc
from collections import Counter
from typing import Dict


def enumerate_microstates(N: int):

    total_states = 1 << N  # Equivalent to 2^N
    
    for i in range(total_states):
        # Extract each bit's value (0 or 1) using right shift (>>) and bitwise AND (&)
        microstate = tuple((i >> j) & 1 for j in range(N))
        yield microstate

def group_macrostates(N: int) -> Dict[int, int]:
    """
    Counts the number of microstates for each macrostate (k heads).
    """
    macrostates = Counter()
    for microstate in enumerate_microstates(N):
        k = sum(microstate)
        macrostates[k] += 1
    return dict(macrostates)

def benchmark_enumeration(max_time_seconds: int = 300) -> None:
    """
    Finds the maximum N computable within a 5 mins limit.
    """
    N = 1
    while True:
        tracemalloc.start()
        start_time = time.time()
        
        # Consume the generator purely to measure traversal cost
        for _ in enumerate_microstates(N):
            pass
            
        elapsed = time.time() - start_time
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"N={N} | Time: {elapsed:.4f}s | Memory: {peak_memory / 1024**2:.4f} MB")
        
        if elapsed > max_time_seconds:
            print(f"Time limit exceeded at N={N}.")
            break
        N += 1