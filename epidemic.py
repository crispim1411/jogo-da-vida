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
BORDER = True

# Variáveis segundo o artigo
K = 0.44
L = 0.04
Tc = 40
T_IN = 5
T_IM = 5

counter = 0

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

def epidemic_value(cell):
    """Retorna valor de transmissão da célula"""
    inf = cell[1]
    imf = cell[2]
    # está imune
    if imf != 0:
        return 0
    # suscetível ou infectada
    return cell[0]

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
    if counter % (T_IN + T_IM) == 0:
        new_world[4*N//5][4*N//5] = np.array([0.1, T_IN, 0])
        new_world[N//5][N//5] = np.array([0.1, T_IN, 0])
        
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
        
        world = tick(world)
        infected[counter] = np.count_nonzero(world[:,:,1])
        immunized[counter] = np.count_nonzero(world[:,:,2])
        counter += 1
    fig.colorbar(im, ax=axes.ravel().tolist())

    # infectados e imunizados
    fig, (ax1, ax2) = plt.subplots(2)
    ax1.title.set_text('Infectados')
    plt.xticks(range(0,Tc,5))
    ax1.plot(infected, 'r-o')
    ax2.title.set_text('Imunizados')
    ax2.plot(immunized, 'b-o')

if __name__ == '__main__':
    # formato do mundo
    # matrix N x N onde cada dado
    # C -> {P; t_in; t_tim}
    world = np.zeros(N*N*3).reshape(N,N,3)

    # seta valores iniciais
    world[0][0] = np.array([0.1, T_IN, 0])
    # world[N//2][N//2] = np.array([0.1, T_IN, 0])

    ani = animation_CA(world)
    gen_plots(world)

    plt.show()
   