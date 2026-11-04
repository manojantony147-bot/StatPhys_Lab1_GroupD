from src.combinatorics import log_omega
import math

def expected_waiting_time(N: int, k_target: int, rate_per_second: int) -> float:
    """
    Calculates the expected time in seconds to randomly observe a 
    specific highly ordered state (e.g., k=8), assuming a given tossing rate.
    """
    # Use log-space to find ln(P_target) = ln(Omega) - N*ln(2)
    ln_p_target = log_omega(N, k_target) - N * math.log(2)
    p_target = math.exp(ln_p_target)
    
    # Expected trials is 1/P. Total time is trials / rate.
    expected_trials = 1.0 / p_target
    return expected_trials / rate_per_second

def entropy_change(N: int, k1: int, k2: int) -> float:
    """Entropy change Delta S = S(k1) - S(k2), in J/K."""
    return calculate_entropy(N, k1) - calculate_entropy(N, k2)