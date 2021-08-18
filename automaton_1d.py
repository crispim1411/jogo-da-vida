import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt

N = 100 # tamanho do vetor
STEPS = 50

def update(vector, rule):
    new_values = np.zeros(N)
    for i in range(N):
        p,q,r = vector[(i-1) % N], vector[i], vector[(i+1) % N]
        if rule(p,q,r):
            new_values[i] = 1
    return new_values

def run (rule, title):
    initial_vector = np.zeros(N)
    initial_vector[N//2] = 1
    B = np.zeros((STEPS, N))
    B[0] = initial_vector.copy()
    values = initial_vector
    for i in range(1, STEPS):
        new_values = update(values, rule)
        B[i] = new_values
        values = new_values

    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.matshow(B, cmap=plt.cm.binary)

rule45 = lambda p,q,r: True if bool(p) ^ bool(q or not r) else False
run(rule45, 'Rule 45')

rule57 = lambda p,q,r: True if bool(p or not r) ^ bool(q) else False
run(rule57, 'Rule 57')

rule90 = lambda p,q,r: True if p != r else False
run(rule90, 'Rule 90')

rule150 = lambda p,q,r: True if (p,q,r).count(1) in [3, 1] else False
run(rule150, 'Rule 150')

plt.show()