import os
import math
import statistics
import importlib
import matplotlib.pyplot as plt

from src.microstates import benchmark_enumeration, enumerate_microstates, group_macrostates
from src.combinatorics import calculate_probability, calculate_cumulative_probability

def task_a_enumeration():
    print("--- Task a: Enumeration for N = 7 ---")
    N = 7
    print(f"Listing all 2^{N} = {1 << N} microstates:")
    for microstate in enumerate_microstates(N):
        print(microstate)
    
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
        plt_mod = importlib.import_module("matplotlib.pyplot")
    except ModuleNotFoundError:
        print("Matplotlib is not installed; skipping the distribution plot.")
        return

    N_values = [20, 50, 80, 100]
    plt_mod.figure(figsize=(10, 6))
    
    for N in N_values:
        k_values = list(range(N + 1))
        omega_values = [math.comb(N, k) for k in k_values]
        plt_mod.plot(k_values, omega_values, marker='o', linestyle='-', markersize=3, label=f"N = {N}")
        
    plt_mod.title(r"Macrostate Frequency Distribution $\Omega(N, k)$", fontsize=12, fontweight='bold')
    plt_mod.xlabel("Number of Heads ($k$)", fontsize=10)
    plt_mod.ylabel(r"Frequency $\Omega(N, k)$", fontsize=10)
    plt_mod.yscale('log')
    plt_mod.legend()
    plt_mod.grid(True, linestyle='--', alpha=0.6)
    plt_mod.tight_layout()
    
    os.makedirs("report/figures", exist_ok=True)
    plt_mod.savefig("report/figures/macrostate_distribution_combined.pdf", format='pdf')
    plt_mod.show()

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

def main_probability_plots():
    figures_dir = "report/figures"
    if os.path.exists(figures_dir) and not os.path.isdir(figures_dir):
        os.remove(figures_dir)
    os.makedirs(figures_dir, exist_ok=True)

    benchmark_enumeration(max_time_seconds=1)

    N_values = [20, 50, 80, 100]
    for N in N_values:
        k_values = list(range(N + 1))
        probabilities = [calculate_probability(N, k) for k in k_values]
        plt.figure(figsize=(8, 5))
        plt.plot(k_values, probabilities, marker='o', linestyle='-', color='teal', markersize=3, linewidth=1.5)
        plt.title(f"Macrostate Probability Distribution ($N = {N}$)", fontsize=12, fontweight='bold')
        plt.xlabel("Number of Heads ($k$)", fontsize=10)
        plt.ylabel("Probability $P_k$", fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()
        output_path = f"report/figures/probability_distribution_N{N}.pdf"
        plt.savefig(output_path, format='pdf', bbox_inches='tight')
        plt.show()
        plt.close()
        print(f" -> Generated and saved: {output_path}")

if __name__ == "__main__":
    task_a_enumeration()
    task_b_benchmark() 
    task_c_distribution()
    solve_section_2([99, 7, 52, 12])
    main_probability_plots()