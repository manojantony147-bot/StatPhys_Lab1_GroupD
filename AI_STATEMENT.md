For this task, it has been used Gemini Pro 3.1. The use of AI was explicitly as code assistant.

Prompt 1: I need you as my code assistant to help me develop a code for the computational analysis of microstates (Also we have uploaded the laboratory guide for more background for the AI).

Gemini:
As your code assistant, I can help you structure the logic and write the core mathematical functions, though you will still need to assemble the final script yourself to align with the written requirement that the code is your team's original work. To tackle the enumeration for N=7, you can use Python's itertools library to generate the discrete microstates. Here is the core logic to get you started:

import itertools
import math

# a) Generate all microstates for N=7
N = 7
# Creates tuples of all possible 2^N configurations
microstates = list(itertools.product(['H', 'T'], repeat=N))

# c) Macrostate Frequency Calculation
def calculate_omega(n, k):
    # Omega(N, k) = N! / (k! * (N-k)!)
    return math.comb(n, k)

For the maximum computable N task, the constraint stems from attempting to store 2^N specific configurations in your system's RAM. To test this and aim for the performance incentive, you can write a loop that generates combinations for increasing values of N, using Python's time module to track when the execution reaches the five-minute wall-clock limit.   How would you like to approach generating the macrostate distribution plot for the larger sets of $N=20, 50, 80$, and $100$?

Prompt 2: use the same approach as before, and then for values higher than 100 it is going to be used the log-gamma function

Gemini: 
Using the log-gamma function is the computationally robust way to prevent integer overflow when calculating multiplicities for systems where $N > 100$, such as your custom $N = 100 + M$ variable. Since the binomial coefficient $\Omega(N,k) = \frac{N!}{k!(N-k)!}$ grows exponentially, taking the natural logarithm converts the factorials into manageable sums via $\ln(x!) = \ln(\Gamma(x+1))$.   Here is how you can implement this in Python using math.lgamma to calculate both the multiplicity and the specific probabilities $P_k$:

import math

def log_omega(n, k):
    # ln(N!) - [ln(k!) + ln((N-k)!)]
    # math.lgamma(x) computes ln(Gamma(x)), and Gamma(x) = (x-1)!
    return math.lgamma(n + 1) - (math.lgamma(k + 1) + math.lgamma(n - k + 1))

def calculate_probability(n, k):
    # P_k = Omega(N,k) / 2^N  ->  ln(P_k) = ln(Omega) - N*ln(2)
    ln_pk = log_omega(n, k) - n * math.log(2)
    return math.exp(ln_pk)

This logarithmic approach bypasses massive integers, allowing you to compute the probability for $k=30$ or the cumulative probabilities $\Delta P_{k_1k_2}$ without crashing your script. Additionally, for the entropy change equations, you can plug the output of log_omega(n, k) directly into the Boltzmann formula $S = k_B \log \Omega$ without exponentiating it back to the raw number of microstates.   Do you want to map out the code to calculate the harmonic average $M$ from your team's NIAs, or move to analyzing the thermodynamic limit as $N \rightarrow \infty$?

Prompt: yes, help me to map out the code to calculate the harmonic average but do not analyze the thermodynamic limit.


Gemini:
To calculate the harmonic average $M$ from the last two digits of your team members' academic identifiers (NIAs) and establish your specific system size $N$, you can use Python's built-in statistics module. Here is the logic to map this out while ensuring $N$ remains below the 200-coin limit:

import statistics

def calculate_system_size(nia_digits):
    # nia_digits: list of the last two digits of each team member's NIA
    # Calculate the harmonic average M
    M = statistics.harmonic_mean(nia_digits)
    
    # Calculate total N = 100 + M
    N = round(100 + M)
    return N


Improvements:
For the microstate counting, when the total states are 1 << N, our code does not do bitwise shifting (as suggested in the guide). For this reason, bitwise shifting (we discard the itertools approach) is done with generators (yield) so that our RAM does not have to store the thousands of values of the microstates:

New code:
def enumerate_microstates(N: int):

    total_states = 1 << N  # Equivalent to 2^N
    
    for i in range(total_states):
        # Extract each bit's value (0 or 1) using right shift (>>) and bitwise AND (&)
        microstate = tuple((i >> j) & 1 for j in range(N))
        yield microstate

For the functions of calculate_omega, log_omega and calculate_probability, the AI has not considered the fact that the functions have to be typed, therefore, the change has only be done in the definition of the function:

def calculate_omega(N: int, k: int) -> int:

def log_omega(N: int, k: int) -> float:

def calculate_probability(N: int, k: int) -> float:

Moreover, some pseudocode has been added so my collegues understand better each of the functions.


Now, a better prompt for the AI was done in order to help me code the grouping of states and the benchmarking.

Prompt: taking into account that the functions have to be typed and that the code of the microstate counting was changed in order to have generators (instead of using the itertool approach), create the code for the grouping of states and the benchmarking.

Gemini:
To handle the grouping of states and the performance benchmarking, append these functions below your generator:

import time
import tracemalloc
from collections import Counter
from typing import Dict

def group_macrostates(N: int) -> Dict[int, int]:
    """
    Counts the number of microstates for each macrostate (k heads).
    Useful for listing outcomes in small systems like N=7.
    """
    macrostates = Counter()
    for microstate in enumerate_microstates(N):
        k = sum(microstate)
        macrostates[k] += 1
    return dict(macrostates)

def benchmark_enumeration(max_time_seconds: int = 300) -> None:
    """
    Finds the maximum N computable within a given time limit (default 5 mins)
    by measuring execution time and peak RAM usage.
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

In this case, no improvements were necessary as with a more clear prompt for the AI the code generated was better.
The code for the cumulative probability, and to calculate the entropy, was not necessary to use AI as it was trivial. For the likelihood_ratio, however, it was necessary to use AI:

Prompt: Using the considerations I told you above, I need that you create a code of the likelihood ratio.

Gemini:
Here is the code generated to obtain the likelihood ratio using your existing log-space math:

def likelihood_ratio(N: int, k_target: int) -> float:
    """
    Quantifies how much more likely the most probable state (N/2) 
    is compared to a target state k, using log-space to prevent overflow.
    """
    k_max = N // 2
    log_ratio = log_omega(N, k_max) - log_omega(N, k_target)
    return math.exp(log_ratio)

Again, no improvements needed.

Finally, the code for the expected waiting time to highly ordered state function was generated.

Prompt: Lastly, I need you to help me build the waiting time to highly ordered state function code.

Gemini:The expected waiting time is the inverse of the target macrostate's probability, which requires keeping the calculation in log-space as long as possible to avoid underflow errors with large $N$.

from combinatorics import log_omega
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
# Main code prompts
Prompt 1: Is this correct for micro state? / Ok is this correct? (submitting user-written code for review)AI Assistance: Instead of generating full modules from scratch, the AI acted as a code reviewer and logic verifier. It validated the correctness of the user's bitwise generator (enumerate_microstates), group_macrostates, log-space combinatorics (log_omega), and the expected_waiting_time function, ensuring they adhered to physical constraints and prevented numerical overflow.
Prompt 2: (Handling Git identity error) / What is the next step? / Can you create a flowchart for main.py? Explain this part.AI Assistance:Resolved a Git identity configuration warning (user.name and user.email).Provided a concise checklist of remaining tasks. High-resolution vector .pdf plot generation into report/figures/.
