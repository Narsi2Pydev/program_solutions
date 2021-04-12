# Python code to implement Conway's Game Of Life
import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# setting up the values for the grid
ON = 255
OFF = 0
vals = [ON, OFF]


def randomGrid(N):
    """
    returns a grid of NxN random values
    :param N:
    :return:
    """
    return np.random.choice(vals, N * N, p=[0.2, 0.8]).reshape(N, N)


def addGlider(row, column, grid):
    """
    adds a glider with top left cell at given row, and column)
    :param row:
    :param column:
    :param grid:
    :return:
    """
    glider = np.array([[0, 0, 255],
                       [255, 0, 255],
                       [0, 255, 255]])
    grid[row:row + 3, column:column + 3] = glider


def addGosperGliderPoint(row, column, grid):
    """
    adds a Gosper Glider point with top left
    cell at given row, and column
    :param row:
    :param column:
    :param grid:
    :return:
    """
    point = np.zeros(11 * 38).reshape(11, 38)

    point[5][1] = point[5][2] = 255
    point[6][1] = point[6][2] = 255

    point[3][13] = point[3][14] = 255
    point[4][12] = point[4][16] = 255
    point[5][11] = point[5][17] = 255
    point[6][11] = point[6][15] = point[6][17] = point[6][18] = 255
    point[7][11] = point[7][17] = 255
    point[8][12] = point[8][16] = 255
    point[9][13] = point[9][14] = 255

    point[1][25] = 255
    point[2][23] = point[2][25] = 255
    point[3][21] = point[3][22] = 255
    point[4][21] = point[4][22] = 255
    point[5][21] = point[5][22] = 255
    point[6][23] = point[6][25] = 255
    point[7][25] = 255

    point[3][35] = point[3][36] = 255
    point[4][35] = point[4][36] = 255

    grid[row:row + 11, column:column + 38] = point


def update(frameNum, img, grid, N):
    """
    copy the  grid , we require only 8 neighbors for calculation and we go line by line
    :param frameNum:
    :param img:
    :param grid:
    :param N:
    :return:
    """
    newGrid = grid.copy()
    for row in range(N):
        for column in range(N):

            # computing the  8-neghbor sum
            total = int((grid[row, (column - 1) % N] + grid[row, (column + 1) % N] +
                         grid[(row - 1) % N, column] + grid[(row + 1) % N, column] +
                         grid[(row - 1) % N, (column - 1) % N] + grid[(row - 1) % N, (column + 1) % N] +
                         grid[(row + 1) % N, (column - 1) % N] + grid[(row + 1) % N, (column + 1) % N]) / 255)

            # apply Conway's rules
            if grid[row, column] == ON:
                if (total < 2) or (total > 3):
                    newGrid[row, column] = OFF
            else:
                if total == 3:
                    newGrid[row, column] = ON

    # updating the data in the grid
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,


# main() function
def main():
    """
    Main function is created to call the grods
    sys.argv[0] is the script name itself and can be ignored
    :return:
    """

    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation.")

    # add arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required=False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()

    # setting the grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)

    # Updating the interval
    updateInterval = 50
    if args.interval:
        updateInterval = int(args.interval)

    # declaring the  grid
    grid = np.array([])

    # check if "glider" demo flag is specified or not
    if args.glider:
        grid = np.zeros(N * N).reshape(N, N)
        addGlider(1, 1, grid)
    elif args.gosper:
        grid = np.zeros(N * N).reshape(N, N)
        addGosperGliderPoint(10, 10, grid)

    else:  # populate grid with random on/off -
        # more off than on
        grid = randomGrid(N)

    # setting up the animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N,),
                                  frames=10,
                                  interval=updateInterval,
                                  save_count=50)

    # displaying the out file
    if args.movfile:
        ani.save(args.movfile, fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()


# calling the main function
if __name__ == '__main__':
    main()
