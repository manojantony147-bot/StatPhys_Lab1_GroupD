import pytest
from unittest.mock import patch
from src.microstates import group_macrostates, enumerate_microstates
from main import task_a_enumeration, task_b_benchmark, task_c_distribution

def test_group_macrostates():
    result = group_macrostates(3)
    assert result == {0: 1, 1: 3, 2: 3, 3: 1}

def test_enumerate_microstates():
    result = list(enumerate_microstates(4))
    assert len(result) == 16

def test_task_a_enumeration(capsys):
    task_a_enumeration()
    captured = capsys.readouterr()
    assert "Task a: Enumeration for N = 7" in captured.out
    assert "Listing all 2^7 = 128 microstates" in captured.out

@patch('main.benchmark_enumeration')
def test_task_b_benchmark(mock_benchmark, capsys):
    task_b_benchmark()
    mock_benchmark.assert_called_once_with(max_time_seconds=300)

@patch('matplotlib.pyplot.show')
@patch('matplotlib.pyplot.savefig')
@patch('os.makedirs')
def test_task_c_distribution(mock_makedirs, mock_savefig, mock_show):
    task_c_distribution()
    mock_makedirs.assert_called_once_with("report/figures", exist_ok=True)
    mock_savefig.assert_called_once_with("report/figures/macrostate_distribution_combined.pdf", format='pdf')
    mock_show.assert_called_once()