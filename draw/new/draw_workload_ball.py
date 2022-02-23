import random
from tqdm import tqdm
import matplotlib.pyplot as plt

def draw_ball(file_name):
    from matplotlib.patches import Circle
    # x, y, r, 2, sel
    DPI = 72
    fig = plt.figure(figsize=(500 / DPI, 500 / DPI), dpi=DPI)
    ax = plt.subplot()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    count = 0

    with open(file_name, 'r') as f:
        node_list = []
        # for i in range(3):
        #     f.readline()
        lines = f.readlines()
        random.shuffle(lines)
        lines = lines[:100]

        for line in tqdm(lines):
            line = line.strip().split(',')
            line = [float(i) for i in line]
            # print(line)
            circle = Circle(xy=(line[0], line[1]), radius=line[2], fill=None)
            ax.add_patch(circle)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.invert_yaxis()
        plt.tight_layout()
        plt.savefig('ball_data_driven_workload.pdf', DPI=72)
        plt.show()
        return


draw_ball('../../data/HighDim/Ball/forest-data-2d-2100.txt')