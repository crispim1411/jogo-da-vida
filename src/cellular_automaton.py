import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

N = 50
SPEED = 100
PROB_LIFE = 40

# frameNum - this is handled by the animation, don't change this.
# img - the plot that is passed and changed, don't change this.
# world - the two-D array that represents the world for the
#         game of life. This will be updated to the next gen.
# N - the size of the world (which is square).


def update(frameNum, img, world, N):
    newWorld = world.copy()

    # TODO: Escrever codigo para atualizar celula no newWorld
    # para proxima geração lembrar de usar modelo toroidal(??) invés de
    # fazer casos especiais para linha/coluna 0 e N-1
    # trocar pelo produto cartesiano
    for i in range(N):
        for j in range(N):
            # opçao sem borda infinita
            total = (
                world[(i-1) % N][(j-1) % N] + world[(i-1) % N][j] + world[(i-1) % N][(j+1) % N] +
                world[i][(j-1) % N] + world[i][(j+1) % N] + world[(i+1) % N][(j-1) % N] +
                world[(i+1) % N][j] + world[(i+1) % N][(j+1) % N])/255

            if world[i][j] == 255:
                if total > 3 or total < 2:
                    newWorld[i][j] = 0
            else:
                if total == 3:
                    newWorld[i][j] = 255

    img.set_data(newWorld)
    world[:] = newWorld[:]
    return img


if __name__ == '__main__':
    # TODO: População inicial invés de randomica
    world = np.random.choice(
        [0, 255],
        N*N,
        p=[1-(PROB_LIFE/100), (PROB_LIFE)/100]
    ).reshape(N, N)

    fig, ax = plt.subplots()
    img = ax.imshow(world, interpolation='nearest')
    a = animation.FuncAnimation(fig, update, fargs=(
        img, world, N), frames=30, interval=SPEED, save_count=50)

    plt.show()
