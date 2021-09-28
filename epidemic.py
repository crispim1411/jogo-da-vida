# cada celula é atualizada simultaneamente em passos discretos
# número de dimensões espaciais -> 2
# comprimento de cada lado do array -> 100x100
# comprimento da vizinhança da célula -> 3x3
# estados das células do AC
# regra de transição

# Os estados são marcados por 
# C(t) = {P(t), INF(t), IMF(t)} (na localização i,j)
# INF flag de infecção 
    # se INF = 1 então 0.0 < P(t) <= 1.0
        # P(t) = S(t) / T(t) infectados/total da célula
    # se INF = 0 então P(t) = 0.0
# Após t_in passos a flag INF passa de 1 para 0
# IMF se torna 1, indicando que a população da célula está imune
# Após t_im a célula se torna sucestível novamente IMF vira 0

# algoritmo
# (1) Inicio
# (2) t = 1
# (3) Lê propriedades iniciais (estado inicial do AC)
# (4) t += 1
# (5) Determina quais célula possuem indivíduos infectados e quais não possuem
# (6) Se IMF = 1 vai pra (8) caso contrário (7)
# (7) Calcula porcentagem P(t) usando regra local
# (8) Se t < Tc vai pra (4) caso contrário calcula output
# (9) Fim

# O estado t+1 é afetado pelas 8 células vizinhas e por seu próprio estado
# Considerando matrix 100x100 
# k = 0.44 e l = 0.04
# Tc = 40 passos
# t_in = 5 e t_im = 10
# 11 estados possíveis para P(t)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation

N = 30
INTERVAl = 1000
FPS = 40

# Variáveis segundo o artigo
K = 0.44
L = 0.04
Tc = 40
T_IN = 5 
T_IM = 10

def to_discrete_value(value):
    """Adequa os valores nos intervalos discretos
    Ex: 0.1 <= 0.122 < 0.2 -> 0.2
    """
    if value >= 0.9:
        return 1.0
    elif value >= 0.8:
        return 0.9
    elif value >= 0.7:
        return 0.8
    elif value >= 0.6:
        return 0.7
    elif value >= 0.5:
        return 0.6
    elif value >= 0.4:
        return 0.5
    elif value >= 0.3:
        return 0.4
    elif value >= 0.2:
        return 0.3
    elif value >= 0.1:
        return 0.2
    elif value > 0.0:
        return 0.1
    else:
        return 0

def gen_world(world):
    fig, ax = plt.subplots()
    ax.grid()
    ax.set_xticks(np.arange(0.5, N))
    ax.set_yticks(np.arange(0.5, N))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    img = ax.imshow(world, interpolation='nearest', vmin=0., vmax=1.)
    plt.colorbar(img)

    return fig, img, world

def epidemic_value(cell):
    """Retorna valor de transmissão da célula"""
    inf = cell[1]
    imf = cell[2]
    # está imune
    if imf != 0:
        return 0
    # suscetível ou infectada
    return cell[0]

def update(frameNum, img, world, N):
    new_world = world.copy()
    for i in range(N):
        for j in range(N):
            # check flags
            inf = world[i][j][1] # infectado
            imf = world[i][j][2] # imunizado

            # disease tick t+1
            if inf > 0:
                if inf == 1:
                    imf = T_IM
                inf -= 1
            elif imf > 0:
                imf -= 1
                
            # atualiza
            new_world[i][j][1] = inf
            new_world[i][j][2] = imf

            # suscetível
            if imf == 0:
                diagonals = epidemic_value(world[(i-1) % N][(j-1) % N]) + \
                            epidemic_value(world[(i-1) % N][(j+1) % N]) + \
                            epidemic_value(world[(i+1) % N][(j-1) % N]) + \
                            epidemic_value(world[(i+1) % N][(j+1) % N]) 
                    
                nearest = epidemic_value(world[(i+1) % N][j]) + \
                          epidemic_value(world[(i-1) % N][j]) + \
                          epidemic_value(world[i][(j+1) % N]) + \
                          epidemic_value(world[i][(j-1) % N])

                cell_value = world[i][j][0]
                value = cell_value + K*nearest + L*diagonals
                if value > 0 and inf == 0:
                    # se torna infectada
                    new_world[i][j][1] = T_IN 
                new_world[i][j][0] = to_discrete_value(value)
            else:
                # está imunizada
                new_world[i][j][0] = 0

            if 12<i<18 and 12<j<18:
                print(f"({i},{j}) / cell:{new_world[i][j]} / nearest:{nearest:.1f} / diagonal:{diagonals:.1f}")

    img.set_data(new_world[:,:,0])
    world[:] = new_world[:]
    
    return img

if __name__ == '__main__':
    # gerando um mundo randômico com estados de 0 a 1.0
    # initial_values = np.random.choice(
    #     [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    #     (N,N,3),
    #     p=[.95, .05, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # ).reshape(N, N, 3)
    initial_values = np.zeros(N*N*3).reshape(N,N,3)
    initial_values[N//2][N//2] = np.array([0.1, T_IN, 0])

    fig, img, world = gen_world(initial_values)

    print(f"Initial state (15,15) / cell: [0.1, {T_IN}, 0.0] / nearest:0.0 / diagonal:0.0")
    ani = animation.FuncAnimation(fig, update, fargs=(
        img, world, N), frames=FPS, interval=INTERVAl)

    plt.show()