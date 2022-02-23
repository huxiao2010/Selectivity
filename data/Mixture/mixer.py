import argparse
import sys
import random
import math

data_path = '../HighDim/'
file_name = {
    'Forest-2d' : ('assertion_forest_2d', 'forest-data-2100-2d'),
    'Power-2d' : ('assertion_power_2d', 'power-data-10000-2d')
}
file_suf = '.txt'
mix_ratios = [0.0, 0.25, 0.5, 0.75, 1.0]

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='Forest-2d', help='[Forest-2d/Power-2d]')
parser.add_argument('--gen', type=str, default="test", help="generate [train/test] set")
parser.add_argument('--train_size', type=int, default=2000, help="size of train set")
parser.add_argument('--test_size', type=int, default=100, help='size of test set')
args = parser.parse_args()

def print_error(msg):
    print("Error: %s" % msg)

def load_dataset(filename, gen, size):
    whole_list = []
    with open(filename, 'r') as fin:
        for line in fin.readlines():
            whole_list.append(line)
    if (gen == "test"):
        return whole_list[-1 - size : -1]
    else:
        return whole_list[:size]

def gen_dataset(filename, gen_set):
    print("===== Generate %s =====" % filename)
    with open(filename, "w") as fout:
        for i in range(len(gen_set)):
            fout.write(gen_set[i])

if __name__ == "__main__":
    random.seed(2022)
    dataset = args.dataset
    gen = args.gen

    if (dataset not in ['Forest-2d', 'Power-2d']):
        print_error("unsupported dataset")
        sys.exit()

    if (gen not in ["train", "test"]):
        print_error("unsupported type of generation")
        sys.exit()

    if (gen == "train"):
        size = args.train_size
    else:
        size = args.test_size
    
    r_file, d_file = file_name[dataset]
    r_file = data_path + r_file + file_suf
    d_file = data_path + d_file + file_suf

    r_dataset = load_dataset(r_file, gen, size)
    d_dataset = load_dataset(d_file, gen, size)

    for num in range(10):
        random.shuffle(r_dataset)
        random.shuffle(d_dataset)

        for ratio in mix_ratios:
            d_num = math.floor(ratio * size)
            r_num = size - d_num
            gen_set = r_dataset[:r_num] + d_dataset[:d_num]
            random.shuffle(gen_set)
            if (gen == "test"):
                filename = "./test/test%d_%s_r%.2f_d%.2f" % (num, dataset, 1 - ratio, ratio)
            else:
                filename = "./train/train%d_%s_tr%d_r%.2f_d%.2f" % (num, dataset, size, 1 - ratio, ratio)
            gen_dataset(filename + file_suf, gen_set)

