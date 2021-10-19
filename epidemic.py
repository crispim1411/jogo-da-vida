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

import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import animation

from utils import to_discrete_value, epidemic_value

N = 100
INTERVAl = 100
FPS = 50
BORDER = True

# Variáveis segundo o artigo
K = 0.44
L = 0.04
Tc = 85
T_IN = 15
T_IM = 30
START_MOVE = 30
perc_moves = 40/100
max_distance = 15

counter = 0

def move(world):
    # considerando que ao mover a população de uma célula irá para outro espaço e este ficará vazio
    # a densidade demográfica se torna não-uniforme
    # enquanto não preencher 10% de movimentados
    # após 30 steps irá ter movimentação
    new_world = world.copy()
    moves_history = []
    while len(moves_history) < round(N*perc_moves):
        x, y = (random.randint(0, N-1), random.randint(0, N-1))
        if (x,y) not in moves_history:
            # apenas infectados se movendo
            # se movendo para fora do centro
            center = N//2
            distance = random.randint(1, max_distance)
            if new_world[x][y][1] != 0:
                # max_distance = 5
                x_direction = 1 if x > center else -1
                x_moved = x + distance * x_direction
                if x_moved < 0:
                    x_moved = 0
                elif x_moved > N-1:
                    x_moved = N-1

                y_direction = 1 if y > center else -1
                y_moved = y + distance * y_direction
                if y_moved < 0:
                    y_moved = 0
                elif y_moved > N-1:
                    y_moved = N-1

                # a -> b
                a = world[x][y]
                b = world[x_moved][y_moved]
                # a se torna vazia
                new_world[x][y] = [0, 0, math.inf]
                new_perc = round((a[0] +b[0])/2, 1)
                if new_perc > 1:
                    new_perc = 1
                new_world[x_moved][y_moved] = [new_perc, T_IN, 0]
                moves_history.append((x, y))
                print(f"{(x,y)} -> {(x_moved,y_moved)} {a} -> {b}: {new_world[x_moved][y_moved]}")
    return new_world

def tick(world):
    """ update world """
    global counter
    counter += 1
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
                if BORDER:
                    diagonals = (epidemic_value(world[i-1][j-1]) if i!=0 and j!=0 else 0) + \
                                (epidemic_value(world[i-1][j+1]) if i!=0 and j!=N-1 else 0) + \
                                (epidemic_value(world[i+1][j-1]) if i!=N-1 and j!=0 else 0)  + \
                                (epidemic_value(world[i+1][j+1]) if i!=N-1 and j!=N-1 else 0)
            
                    nearest = (epidemic_value(world[i+1][j]) if i!=N-1 else 0) + \
                            (epidemic_value(world[i-1][j]) if i!=0 else 0) + \
                            (epidemic_value(world[i][j+1]) if j!=N-1 else 0) + \
                            (epidemic_value(world[i][j-1]) if j!=0 else 0)
                else:
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

    # Após completar o ciclo infectado imunizado 
    # o centro volta a ser infectado
    # if counter % (T_IN + T_IM) == 0:
    #     new_world[4*N//5][4*N//5] = np.array([0.1, T_IN, 0])
    #     new_world[N//5][N//5] = np.array([0.1, T_IN, 0])

    # após 30 steps movimenta
    # if counter == START_MOVE:
    #     new_world = move(new_world)
        
    return new_world

def update(frameNum, img, world, N):
    new_world = tick(world)
    img.set_data(new_world[:,:,0])
    world[:] = new_world[:]
    
    return img

def animation_CA(world):
    fig, ax = plt.subplots()
    ax.grid()
    ax.set_xticks(np.arange(0.5, N))
    ax.set_yticks(np.arange(0.5, N))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    img = ax.imshow(world, vmin=0., vmax=1.)
    fig.colorbar(img)
    ani = animation.FuncAnimation(fig, update, fargs=(img, world, N), frames=15, interval=INTERVAl)
    return ani

def iterate(world):
    global counter
    # definição das variáveis de plotagem
    fig, axes = plt.subplots(2,2)
    gen_axes = (a for a in axes.ravel().tolist())
    infected = np.ndarray(Tc)
    immunized = np.ndarray(Tc)

    plot_counter = 1
    for i in range(Tc):
        if i % 18 == 0 and plot_counter<=4:
            ax = next(gen_axes) 
            ax.grid()
            ax.set_xticks(np.arange(0.5, N))
            ax.set_yticks(np.arange(0.5, N))
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.title.set_text(f'Step {counter}')
            im = ax.imshow(world[:,:,0], cmap='Greys')
            plot_counter += 1
        
        infected[counter] = np.count_nonzero(world[:,:,1])
        immunized[counter] = np.count_nonzero(world[:,:,2])
        world = tick(world)
        # counter += 1
    fig.colorbar(im, ax=axes.ravel().tolist())

    # infectados e imunizados
    fig, (ax1, ax2) = plt.subplots(2)
    plt.xticks(range(0,Tc,5))
    # ax1.title.set_text('Infectados')
    ax1.plot(infected, 'r-o')
    ax1.set_xlabel('Steps')
    ax1.set_ylabel('Infectados')
    # ax2.title.set_text('Imunizados')
    ax2.plot(immunized, 'b-o')
    ax2.set_xlabel('Steps')
    ax2.set_ylabel('Imunizados')

if __name__ == '__main__':
    # formato do mundo
    # matrix N x N onde cada dado
    # C -> {P; c_in; c_tim}
    world = np.zeros(N*N*3).reshape(N,N,3)

    # seta valores iniciais
    # world[0][0] = np.array([0.1, T_IN, 0])
    world[N//2][N//2] = np.array([0.1, T_IN, 0])
    # world[4*N//5][4*N//5] = np.array([0.1, T_IN, 0])
    # world[N//5][N//5] = np.array([0.1, T_IN, 0])

    ani = animation_CA(world)
    #iterate(world)

    plt.show()
   