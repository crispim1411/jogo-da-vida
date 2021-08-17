import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt

# Automato Rule 18
# s(t+1,x) = s(t,x-1) xor s(t,x) xor (s(t,x+1))

tv = 100 # tamanho do vetor
steps = 100
def update():
    # import pdb; pdb.set_trace()
    a = np.zeros(tv) # estado atual das células
    new_a = np.zeros(tv) # novo estado das células
    a = np.around(rand(tv)) # vetor de 0 e 1
    # a = np.array([0,0,0,0,0,1,0,0,0,0])

    B = np.zeros((steps, tv))
    B[0] = a.copy()
    g = 1 # geração atual
    while g < steps:
        # import pdb; pdb.set_trace()
        new_a = np.zeros(tv)
        for i in range(0, tv):
            p,q,r = a[(i-1) % tv], a[i], a[(i+1) % tv]
            if (p,q,r) in [(1,0,0), (0,0,1)]:
                new_value = 1
            else:
                new_value = 0
            new_a[i] = new_value
        a = new_a.copy()
        B[g] = a.copy()
        g += 1
    return B

m = update()
plt.imshow(m)
plt.show()


