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

def run (rule, title, random=False):
    if random:
        initial_vector = np.around(rand(N))
    else:
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


rule160 = lambda p,q,r: True if p and r else False
run(rule160, 'Regra 160 - Classe 1', random=True)

rule90 = lambda p,q,r: True if (p + r) % 2 else False
run(rule90, 'Regra 90 - Classe 2')

rule75 = lambda p,q,r: True if bool(p) ^ bool(not q or r) else False
run(rule75, 'Regra 75 - Classe 3')

rule110 = lambda p,q,r: True if bool(not p and q and r) ^ bool(q) ^ bool(r) else False
run(rule110, 'Regra 110 - Classe 4')

plt.show()