import statistics

if __package__ in (None, ""):
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.combinatorics import calculate_probability, calculate_cumulative_probability
from src.thermodynamics import expected_waiting_time


def solve_section_2(nia_digits: list):
    M = statistics.harmonic_mean(nia_digits)
    N = round(100 + M)

    print(f"Team NIAs last digits: {nia_digits}")
    print(f"Harmonic average M: {M:.4f}")
    print(f"System Size N: {N}\n")

    p_30 = calculate_probability(N, 30)
    print(f"a) P(k = 30) = {p_30:.6e}")


    k_most = N // 2
    p_most = calculate_probability(N, k_most)
    print(f"b) P(k = N/2 [k={k_most}]) = {p_most:.6f}")


    k1_c = k_most - 10
    k2_c = k_most + 10
    cum_c = calculate_cumulative_probability(N, k1_c, k2_c)
    print(f"c) Cumulative P (k from {k1_c} to {k2_c}) = {cum_c:.6f}")

    k1_d = k_most - 20
    k2_d = k_most + 20
    cum_d = calculate_cumulative_probability(N, k1_d, k2_d)
    print(f"d) Cumulative P (tails range equivalent to heads {k1_d} to {k2_d}) = {cum_d:.6f}")


def test_probability_distribution_is_normalized():
    assert abs(sum(calculate_probability(4, k) for k in range(5)) - 1) < 1e-12


def test_known_probability_and_cumulative_probability():
    assert abs(calculate_probability(4, 2) - 0.375) < 1e-12
    assert abs(calculate_cumulative_probability(4, 1, 3) - 0.875) < 1e-12


def test_expected_waiting_time():
    assert abs(expected_waiting_time(4, 1, 1) - 4.0) < 1e-12


if __name__ == "__main__":
    sample_nias = [99, 7, 52, 12]
    solve_section_2(sample_nias)