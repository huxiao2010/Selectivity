import argparse
import sys
import random
import math

file_name = {
    'Forest-2d' : ('../forest/assertion_forest_2d', '../data_sensitive/forest-data-2100-2d'),
    'Power-2d' : ('../power/power-2d-10001', '../data_sensitive/power-data-10000-2d')
}
file_suf = '.txt'
mix_ratios = [0.0, 0.25, 0.5, 0.75, 1.0]

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='Forest-2d', help='[Forest-2d/Power-2d]')
parser.add_argument('--test_size', type=int, default=100, help='size of test set')
args = parser.parse_args()

def print_error(msg):
    print("Error: %s" % msg)

def load_testset(filename, size):
    whole_list = []
    with open(filename, 'r') as fin:
        for line in fin.readlines():
            whole_list.append(line)
    return whole_list[-1 - size : -1]

def gen_testfile(filename, testset):
    print("===== Generate %s =====" % filename)
    with open(filename, "w") as fout:
        for i in range(len(testset)):
            fout.write(testset[i])

if __name__ == "__main__":
    dataset = args.dataset
    test_size = args.test_size

    if (dataset not in ['Forest-2d', 'Power-2d']):
        print_error("unsupported dataset")
        sys.exit()
    
    r_file, d_file = file_name[dataset]
    r_file = r_file + file_suf
    d_file = d_file + file_suf

    r_testset = load_testset(r_file, test_size)
    d_testset = load_testset(d_file, test_size)

    random.seed(2022)
    random.shuffle(r_testset)
    random.shuffle(d_testset)

    for ratio in mix_ratios:
        d_num = math.floor(ratio * test_size)
        r_num = test_size - d_num
        testset = r_testset[:r_num] + d_testset[:d_num]
        gen_testfile("%s_r%.2f_d%.2f" % (dataset, 1 - ratio, ratio) + file_suf, testset)

