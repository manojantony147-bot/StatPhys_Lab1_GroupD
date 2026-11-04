import math

import pytest

from src.combinatorics import calculate_omega
from src.thermodynamics import entropy_change

N = 116
K_B = 1.380649e-23  # J/K (valor exacto SI)
K_MAX = N // 2      # 58

CASES = [
    ("e", K_MAX + 25, K_MAX, -1.523549e-22),
    ("f", K_MAX + 10, K_MAX, -2.371655e-23),
    ("g", K_MAX, 20, 3.700476e-22),
]


@pytest.mark.parametrize("label, k1, k2, expected", CASES)
def test_entropy_change_matches_exact_integers(label, k1, k2, expected):
    """Log-space result must agree with exact integer combinatorics."""
    dS = entropy_change(N, k1, k2)
    exact = K_B * (math.log(calculate_omega(N, k1)) - math.log(calculate_omega(N, k2)))
    assert dS == pytest.approx(exact, rel=1e-12)
    assert dS == pytest.approx(expected, rel=1e-6)


def test_entropy_signs():
    """Moving away from N/2 lowers entropy; moving towards it raises it."""
    assert entropy_change(N, K_MAX + 25, K_MAX) < 0
    assert entropy_change(N, K_MAX + 10, K_MAX) < 0
    assert entropy_change(N, K_MAX, 20) > 0

from src.thermodynamics import expected_waiting_time
from src.combinatorics import likelihood_ratio

# ── h) Tiempo para estado muy ordenado ──────────────────────────────────────
def test_waiting_time_is_astronomically_large():
    """k=8 es tan improbable que el tiempo de espera supera la edad del universo."""
    t = expected_waiting_time(N, k_target=8, rate_per_second=N)
    age_of_universe_s = 4.35e17  # ~13.8 mil millones de años en segundos
    assert t > age_of_universe_s

def test_waiting_time_value():
    """Verifica el valor numérico concreto."""
    t = expected_waiting_time(N, k_target=8, rate_per_second=N)
    # Calculado: 1 / (116 * P(116,8)) en segundos
    import math
    from src.combinatorics import log_omega
    ln_p = log_omega(N, 8) - N * math.log(2)
    expected = math.exp(-ln_p) / N
    assert t == pytest.approx(expected, rel=1e-10)

# ── i) Likelihood ratio ──────────────────────────────────────────────────────
def test_likelihood_ratio_N2_vs_N2_plus_10():
    """El estado N/2 es mucho más probable que N/2+10."""
    ratio = likelihood_ratio(N, K_MAX + 10)
    assert ratio > 1.0  # N/2 siempre más probable

def test_likelihood_ratio_symmetry():
    """Por simetría, ratio(N/2+10) == ratio(N/2-10)."""
    ratio_plus  = likelihood_ratio(N, K_MAX + 10)
    ratio_minus = likelihood_ratio(N, K_MAX - 10)
    assert ratio_plus == pytest.approx(ratio_minus, rel=1e-12)

def test_likelihood_ratio_value():
    """Verifica el valor numérico del ratio para k = N/2 ± 10."""
    ratio = likelihood_ratio(N, K_MAX + 10)
    # Calculado manualmente con log_omega
    import math
    from src.combinatorics import log_omega
    expected = math.exp(log_omega(N, K_MAX) - log_omega(N, K_MAX + 10))
    assert ratio == pytest.approx(expected, rel=1e-12)