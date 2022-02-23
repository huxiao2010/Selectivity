import random
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

def draw_ball(file_name):
    # x1, y1, x2, y2, sel
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

        # theta 1, theta 2, b
        for line in tqdm(lines):
            line = line.strip().split(',')
            line = [float(i) for i in line]
            # x = np.linspace(0, 1, 100)
            # print([0, line[2] / line[1]], [1, ( - line[0] + line[2]) / line[1]])
            ax.plot([0, 1], [line[2] / line[1], (- line[0] + line[2]) / line[1]], color='k')
            # ax.plot([0, 0], [1, 1], color='k')
        ax.set_xticks([])
        ax.set_yticks([])
        # ax.invert_yaxis()
        plt.tight_layout()
        plt.savefig('hf_data_driven_workload.pdf', DPI=72)
        plt.show()
        return


draw_ball('../../data/HighDim/Halfspace/forest-data-2d-2100.txt')