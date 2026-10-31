import math

def calculate_omega(N: int, k: int) -> int:
    """
    Computes Omega.
    Used for small N.
    """
    return math.comb(N, k)


def log_omega(N: int, k: int) -> float:
    """
    Computes the natural logarithm of the Omega using the 
    log-gamma function to prevent integer overflow for large N.
    """
    return math.lgamma(N + 1) - (math.lgamma(k + 1) + math.lgamma(N - k + 1))

def calculate_probability(N: int, k: int) -> float:
    """
    Calculates the probability of a macrostate k for a system of size N 
    using log-space arithmetic to handle large exponentials.
    """
    ln_pk = log_omega(N, k) - N * math.log(2)
    return math.exp(ln_pk)

def calculate_cumulative_probability(N: int, k1: int, k2: int) -> float:
    """
    Calculates the cumulative probability of obtaining between k1 and k2 heads.
    """
    return sum(calculate_probability(N, k) for k in range(k1, k2 + 1))

def calculate_entropy(N: int, k: int, k_B: float = 1.380649e-23) -> float:
    """
    Calculates the entropy S = k_B * ln(Omega) of a specific macrostate.
    """
    return k_B * log_omega(N, k)

def likelihood_ratio(N: int, k_target: int) -> float:
    """
    Quantifies how much more likely the most probable state (N/2) 
    is compared to a target state k, using log-space to prevent overflow.
    """
    k_max = N // 2
    log_ratio = log_omega(N, k_max) - log_omega(N, k_target)
    return math.exp(log_ratio)