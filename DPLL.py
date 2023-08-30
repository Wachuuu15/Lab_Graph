import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import itertools
import random
import time

def brute_force(cnf):
    literals = set()
    for conj in cnf:
        for disj in conj:
            literals.add(disj[0])
 
    literals = list(literals)
    n = len(literals)
    for seq in itertools.product([True,False], repeat=n):
        a = set(zip(literals, seq))
        if all([bool(disj.intersection(a)) for disj in cnf]):
            return True, a
 
    return False, None

def select_literal(cnf):
    for c in cnf:
        for literal in c:
            return literal[0]
 
def dpll(cnf, assignments={}):
 
    if len(cnf) == 0:
        return True, assignments
 
    if any([len(c)==0 for c in cnf]):
        return False, None
    
    l = select_literal(cnf)
 
    new_cnf = [c for c in cnf if (l, True) not in c]
    new_cnf = [c.difference({(l, False)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: True}})
    if sat:
        return sat, vals
         
    new_cnf = [c for c in cnf if (l, False) not in c]
    new_cnf = [c.difference({(l, True)}) for c in new_cnf]
    sat, vals = dpll(new_cnf, {**assignments, **{l: False}})
    if sat:
        return sat, vals
 
    return False, None

def random_kcnf(n_literals, n_conjuncts, k=3):
    result = []
    for _ in range(n_conjuncts):
        conj = set()
        for _ in range(k):
            index = random.randint(0, n_literals)
            conj.add((
                str(index).rjust(10, '0'),
                bool(random.randint(0,2)),
            ))
        result.append(conj)
    return result

if __name__ == "__main__":
    brute_force_times = []
    dpll_times = []
    
    # Experiment over different numbers of literals
    for n_literals in range(16):
        current_brute_force_times = []
        current_dpll_times = []
        
        # Run the experiment 100 times for each number of literals
        for _ in range(100):
            n_conjuncts = random.randint(0, n_literals*6)
            s = random_kcnf(n_literals, n_conjuncts)
            
            # Measure time for brute force
            start = time.time()
            brute_force(s)
            stop = time.time()
            current_brute_force_times.append(stop-start)
            
            # Measure time for DPLL
            start = time.time()
            dpll(s)
            stop = time.time()
            current_dpll_times.append(stop-start)
        
        # Calculate average times and store in lists
        brute_force_times.append(np.mean(current_brute_force_times))
        dpll_times.append(np.mean(current_dpll_times))
    
    # Create a DataFrame to store the results
    df = pd.DataFrame(
        {'Number of literals': range(16),
         'Brute Force': brute_force_times,
         'DPLL': dpll_times
        }
    )
    
    sns.set()
    # Plotting
    viz = df.plot(x='Number of literals')
    viz.set_ylabel("Time (Seconds)")
    plt.title("Comparison of Brute Force and DPLL Algorithms")
    plt.show()
