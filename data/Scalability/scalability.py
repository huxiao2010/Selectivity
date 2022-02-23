import argparse
import sys
import random
import math

data_path = '../HighDim/'
file_name = 'assertion_power_2d'
file_suf = '.txt'

def load_dataset(filename):
    whole_list = []
    with open(filename, 'r') as fin:
        for line in fin.readlines():
            whole_list.append(line)
    return whole_list

def gen_dataset(filename, gen_set):
    print("===== Generate %s =====" % filename)
    with open(filename, "w") as fout:
        for i in range(len(gen_set)):
            fout.write(gen_set[i])

if __name__ == "__main__":
    random.seed(2022)
    test_size = 100
    train_size = 2000

    full_list = load_dataset(data_path + file_name + file_suf)
    test_list = full_list[-1 - test_size : -1]
    gen_dataset("test_Power-2d.txt", test_list)

    for num in range(5):
        random.shuffle(full_list)
        train_list = full_list[:train_size]
        gen_dataset("train%d_Power-2d.txt" % (num), train_list)

