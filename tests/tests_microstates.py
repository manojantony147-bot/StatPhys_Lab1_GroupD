import sys
import os
# Add the parent directory (project root) to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import math
import importlib
from src import benchmark_enumeration, enumerate_microstates, group_macrostates

def task_a_enumeration():
    print("--- Task a: Enumeration for N = 7 ---")
    N = 7
    # 1. List all microstates
    print(f"Listing all 2^{N} = {1 << N} microstates:")
    for microstate in enumerate_microstates(N):
        print(microstate)

    # 2. State corresponding number of microstates for each macrostate
    print("\nNumber of microstates per macrostate (k heads):")
    macrostates = group_macrostates(N)
    for k, count in sorted(macrostates.items()):
        print(f"k = {k}: {count} microstates")

def task_b_benchmark():
    print("\n--- Task b: Maximum Computable N (Full Enumeration) ---")
    print("Starting 5-minute benchmark... (This will take up to 300 seconds)")
    benchmark_enumeration(max_time_seconds=300)

def task_c_distribution():
    print("\n--- Task c: Macrostate Frequency Calculation ---")
    try:
        plt = importlib.import_module("matplotlib.pyplot")
    except ModuleNotFoundError:
        print("Matplotlib is not installed; skipping the distribution plot.")
        return

    N_values = [20, 50, 80, 100]
    plt.figure(figsize=(10, 6))

    for N in N_values:
        k_values = list(range(N + 1))
        # Calculating Ω(N, k) using binomial coefficients N choose k
        omega_values = [math.comb(N, k) for k in k_values]
        plt.plot(k_values, omega_values, marker='o', linestyle='-', markersize=3, label=f"N = {N}")

    plt.title(r"Macrostate Frequency Distribution $\Omega(N, k)$", fontsize=12, fontweight='bold')
    plt.xlabel("Number of Heads ($k$)", fontsize=10)
    plt.ylabel(r"Frequency $\Omega(N, k)$", fontsize=10)
    plt.yscale('log') # Log scale is recommended due to massive frequency differences
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    import os
    os.makedirs("report/figures", exist_ok=True)
    plt.savefig("report/figures/macrostate_distribution_combined.pdf", format='pdf')
    plt.show()

if __name__ == "__main__":
    task_a_enumeration()
    task_b_benchmark()
    task_c_distribution()


def test_enumerate_microstates():
    microstates = list(enumerate_microstates(3))

    assert len(microstates) == 8
    assert len(set(microstates)) == 8


def test_group_macrostates():
    assert group_macrostates(3) == {0: 1, 1: 3, 2: 3, 3: 1}
