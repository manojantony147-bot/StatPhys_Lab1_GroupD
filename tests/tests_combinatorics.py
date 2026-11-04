import pytest
from src.combinatorics import calculate_probability, calculate_cumulative_probability
from src.thermodynamics import expected_waiting_time
from main import solve_section_2

def test_solve_section_2_output(capsys):
    solve_section_2([99, 7, 52, 12])
    captured = capsys.readouterr()
    assert "System Size N:" in captured.out
    assert "Harmonic average M:" in captured.out

def test_probability_distribution_is_normalized():
    assert abs(sum(calculate_probability(4, k) for k in range(5)) - 1) < 1e-12

def test_known_probability_and_cumulative_probability():
    assert abs(calculate_probability(4, 2) - 0.375) < 1e-12
    assert abs(calculate_cumulative_probability(4, 1, 3) - 0.875) < 1e-12

def test_expected_waiting_time():
    assert abs(expected_waiting_time(4, 1, 1) - 4.0) < 1e-12