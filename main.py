import os
import matplotlib.pyplot as plt
from src import benchmark_enumeration, calculate_probability


def main():
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
    main()

