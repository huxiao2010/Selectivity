import csv
import numpy as np
import sys
import math
from geometry import HDPoint, Hyperball, Hypercube, Hyperhalfspace

data_path = {'DMV' : '../data/DMV/', 'Instacart' : '../data/Instacart/', 'Power': '../data/workload/'}
query_filename = {'DMV' : 'assertion_dmv.txt', 'Instacart' : 'assertion_instacart.txt', 'Power': "power-nolow.txt"}
min_max_filename = {'DMV' : 'permanent_assertion_dmv.txt',
                    'Instacart' : 'permanent_assertion_instacart.txt',
                    'Power': 'permanent_assertion_power.txt'}
norm_data_path = {'DMV': '../tables/norm/dmv/',
                  'Instacart': '../tables/norm/Instacart/',
                  'Power': '../tables/norm/power/'}
norm_tables = {'DMV': "Dmv.csv", 'Power': "Power.csv"}


# half-space dataset
halfspace_query_path = '../data/HighDim/Halfspace/'
halfspace_query_filename = {'Forest-2d' : 'forest-2d-2100.txt',
                            'Forest-4d' : 'forest-4d-2100.txt',
                            'Forest-6d' : 'forest-6d-2100.txt',
                            'Forest-8d' : 'forest-8d-2100.txt',
                            'Forest-10d' : 'forest-10d-2100.txt',
                            'Forest-2d-data': 'forest-data-2d-2100.txt',
                            'Forest-4d-data': 'forest-data-4d-2100.txt',
                            'Forest-6d-data': 'forest-data-6d-2100.txt',
                            'Forest-10d-data': 'forest-data-10d-2100.txt',
                            'Forest-8d-data': 'forest-data-8d-2100.txt',
                            }
halfspace_min_max_path = '../data/HighDim/'
halfspace_min_max_filename = {'Forest-2d' : 'permanent_assertion_2d.txt',
                              'Forest-4d' : 'permanent_assertion_4d.txt',
                              'Forest-6d' : 'permanent_assertion_6d.txt',
                              'Forest-8d' : 'permanent_assertion_8d.txt',
                              'Forest-10d' : 'permanent_assertion_10d.txt',
                              'Forest-2d-data': 'permanent_assertion_2d.txt',
                              'Forest-4d-data': 'permanent_assertion_4d.txt',
                              'Forest-6d-data': 'permanent_assertion_6d.txt',
                              'Forest-8d-data': 'permanent_assertion_8d.txt',
                              'Forest-10d-data': 'permanent_assertion_10d.txt',
                              }

# ball dataset
ball_query_path = '../data/HighDim/Ball/'
ball_query_filename = {'Forest-2d' : 'forest-2d-2100.txt',
                       'Forest-4d' : 'forest-4d-2100.txt',
                       'Forest-6d' : 'forest-6d-2100.txt',
                       'Forest-8d' : 'forest-8d-2100.txt',
                       'Forest-10d' : 'forest-10d-2100.txt',
                       'Forest-2d-data': 'forest-data-2d-2100.txt',
                       'Forest-4d-data': 'forest-data-4d-2100.txt',
                       'Forest-6d-data': 'forest-data-6d-2100.txt',
                       'Forest-10d-data': 'forest-data-10d-2100.txt',
                       'Forest-8d-data': 'forest-data-8d-2100.txt',
                       }
ball_min_max_path = '../data/HighDim/'
ball_min_max_filename = {'Forest-2d' : 'permanent_assertion_2d.txt',
                         'Forest-4d' : 'permanent_assertion_4d.txt',
                         'Forest-6d' : 'permanent_assertion_6d.txt',
                         'Forest-8d' : 'permanent_assertion_8d.txt',
                         'Forest-10d' : 'permanent_assertion_10d.txt',
                         'Forest-2d-data': 'permanent_assertion_2d.txt',
                         'Forest-4d-data': 'permanent_assertion_4d.txt',
                         'Forest-6d-data': 'permanent_assertion_6d.txt',
                         'Forest-8d-data': 'permanent_assertion_8d.txt',
                         'Forest-10d-data': 'permanent_assertion_10d.txt',
                         }

# high dimension dataset (rect)

hd_data_path = '../data/HighDim/'
hd_query_filename = {'Power-2d': 'assertion_power_2d.txt',
                     'Power-2d-old': 'old_ power_2d_10001.txt',
                     'Power-3d': 'assertion_power_3d.txt',
                     'Power-5d': 'assertion_power_5d.txt',
                     'Power-7d': 'assertion_power_7d.txt',
                     'Power-2d-data': 'power-data-10000-2d.txt',
                     'Power-3d-data': 'power-data-10000-3d.txt',
                     'Power-5d-data': 'power-data-10000-5d.txt',
                     'Power-7d-data': 'power-data-10000-7d.txt',
                     'Power-2d-gauss': 'gauss/power-gauss-2100-2d.txt',
                     'Forest-2d': 'assertion_forest_2d.txt',
                     'Forest-3d': 'assertion_forest_3d.txt',
                     'Forest-4d': 'assertion_forest_4d.txt',
                     'Forest-5d': 'assertion_forest_5d.txt',
                     'Forest-8d': 'assertion_forest_8d.txt',
                     'Forest-10d': 'assertion_forest_10d.txt',
                     'Forest-2d-data': 'forest-data-10000-2d.txt',
                     'Forest-3d-data': 'forest-data-10000-3d.txt',
                     'Forest-4d-data': 'forest-data-10000-4d.txt',
                     'Forest-5d-data': 'forest-data-10000-5d.txt',
                     'Forest-6d-data': 'forest-data-10000-6d.txt',
                     'Forest-10d-data': 'forest-data-10000-10d.txt',
                     'Forest-8d-data': 'forest-data-10000-8d.txt',
                     'Forest-2d-gauss': 'gauss/forest-gauss-2100-2d.txt',
                     'Forest-4d-gauss': 'gauss/forest-gauss-2100-4d.txt',
                     'Forest-6d-gauss': 'gauss/forest-gauss-2100-6d.txt',
                     'Forest-8d-gauss': 'gauss/forest-gauss-2100-8d.txt',
                     'Forest-10d-gauss': 'gauss/forest-gauss-2100-10d.txt',
                     'Census-2d': 'census-data-2100-2d.txt',
                     'DMV-2d': 'dmv-data-2100-2d.txt'}
hd_min_max_filename = {'Power-2d': 'permanent_assertion_2d.txt',
                       'Power-2d-old': 'permanent_assertion_2d.txt',
                       'Power-3d': 'permanent_assertion_3d.txt',
                       'Power-5d': 'permanent_assertion_5d.txt',
                       'Power-7d': 'permanent_assertion_7d.txt',
                       'Power-2d-gauss': 'permanent_assertion_2d.txt',
                       'Power-2d-data': 'permanent_assertion_2d.txt',
                       'Power-3d-data': 'permanent_assertion_3d.txt',
                       'Power-5d-data': 'permanent_assertion_5d.txt',
                       'Power-7d-data': 'permanent_assertion_7d.txt',
                       'Forest-2d-data': 'permanent_assertion_2d.txt',
                       'Forest-4d-data': 'permanent_assertion_4d.txt',
                       'Forest-6d-data': 'permanent_assertion_6d.txt',
                       'Forest-8d-data': 'permanent_assertion_8d.txt',
                       'Forest-10d-data': 'permanent_assertion_10d.txt',
                       'Forest-2d': 'permanent_assertion_2d.txt',
                       'Forest-4d': 'permanent_assertion_4d.txt',
                       'Forest-6d': 'permanent_assetion_6d.txt',
                       'Forest-8d': 'permanent_assertion_8d.txt',
                       'Forest-2d-gauss': 'permanent_assertion_2d.txt',
                       'Forest-4d-gauss': 'permanent_assertion_4d.txt',
                       'Forest-6d-gauss': 'permanent_assertion_6d.txt',
                       'Forest-8d-gauss': 'permanent_assertion_8d.txt',
                       'Forest-10d-gauss': 'permanent_assertion_10d.txt',
                       'Census-2d': 'permanent_assertion_2d.txt',
                       'DMV-2d': 'permanent_assertion_2d.txt'}

epsilon = 0.0001

def print_error(msg):
    print("Error: %s" % msg)

def load_rect(dataset, train_size, test_size):
    # input rect w./wo. card : bl[0], bl[1], tr[0], tr[1], card
    if (dataset not in hd_query_filename) or (dataset not in hd_min_max_filename):
        print_error("unsupported dataset")
        sys.exit()

    cur_data_path = hd_data_path
    cur_query_filename = hd_query_filename[dataset]
    cur_min_max_filename = hd_min_max_filename[dataset]

    whole_list = []
    dim = -1
    with open(cur_data_path + cur_query_filename, 'r') as fin:
        for line in fin.readlines():
            terms = line.strip().split(',')
            dim = (len(terms) - 1) // 2
            bl = []
            tr = []
            for i in range(dim):
                a, b = float(terms[i]), float(terms[dim + i])
                if b < a:
                    a, b = b, a
                bl.append(a)
                tr.append(b)
            whole_list.append([bl, tr, float(terms[len(terms) - 1])])
    if dim != 2:
        print_error("unsupported dataset")
        sys.exit()
    if train_size + test_size > len(whole_list):
        print_error("deficient data size (%d)" % (len(whole_list)))
        sys.exit()

    train_list = whole_list[ : train_size]
    test_list = whole_list[-1 - test_size : -1]

    with open(cur_data_path + cur_min_max_filename, 'r') as fin:
        line = fin.read()
    
    terms = line.strip().split(',')
    bl = []
    tr = []
    for i in range(dim):
        a, b = float(terms[i]), float(terms[dim + i])
        if b < a:
            a, b = b, a
        bl.append(a)
        tr.append(b)
    min_max_rect = [bl, tr]

    return min_max_rect, train_list, test_list

""" deprecated for driver_mixtest.py
def load_mixture_rect(input):
    test_list = []
    with open(input, 'r') as fin:
        for line in fin.readlines():
            terms = line.strip().split(',')
            dim = (len(terms) - 1) // 2
            bl = []
            tr = []
            for i in range(dim):
                a, b = float(terms[i]), float(terms[dim + i])
                if b < a:
                    a, b = b, a
                bl.append(a)
                tr.append(b)
            test_list.append([bl, tr, float(terms[len(terms) - 1])])
    return test_list """

def load_hypercube(dataset, train_size, test_size):
    # input hypercube w./wo. card : bl[0], bl[1], ..., bl[k - 1], tr[0], tr[1], ..., tr[k - 1], card
    if (dataset not in hd_query_filename) or (dataset not in hd_min_max_filename):
        print_error("unsupported dataset")
        sys.exit()
    cur_data_path = hd_data_path
    cur_query_filename = hd_query_filename[dataset]
    cur_min_max_filename = hd_min_max_filename[dataset]

    whole_list = []
    dim = -1
    with open(cur_data_path + cur_query_filename, 'r') as fin:
        for line in fin.readlines():
            terms = line.strip().split(',')
            dim = (len(terms) - 1) // 2
            bl = []
            tr = []
            for i in range(dim):
                a, b = float(terms[i]), float(terms[dim + i])
                if b < a:
                    a, b = b, a
                bl.append(a)
                tr.append(b)
            hypercube = Hypercube(dim, bl, tr)
            whole_list.append([hypercube, float(terms[len(terms) - 1])])
    if train_size + test_size > len(whole_list):
        print_error("deficient data size (%d)" % (len(whole_list)))
        sys.exit()

    train_list = whole_list[ : train_size]
    test_list = whole_list[-1 - test_size : -1]

    with open(cur_data_path + cur_min_max_filename, 'r') as fin:
        line = fin.read()
    
    terms = line.strip().split(',')
    bl = []
    tr = []
    for i in range(dim):
        a, b = float(terms[i]), float(terms[dim + i])
        if b < a:
            a, b = b, a
        bl.append(a)
        tr.append(b)
    root_hc = Hypercube(dim, bl, tr)

    return root_hc, dim, train_list, test_list

def load_mixture_train_hypercube(input):
    # input hypercube w./wo. card : bl[0], bl[1], ..., bl[k - 1], tr[0], tr[1], ..., tr[k - 1], card
    train_list = []
    dim = -1
    with open(input, 'r') as fin:
        for line in fin.readlines():
            terms = line.strip().split(',')
            dim = (len(terms) - 1) // 2
            bl = []
            tr = []
            for i in range(dim):
                a, b = float(terms[i]), float(terms[dim + i])
                if b < a:
                    a, b = b, a
                bl.append(a)
                tr.append(b)
            hypercube = Hypercube(dim, bl, tr)
            train_list.append([hypercube, float(terms[len(terms) - 1])])

    with open('../data/HighDim/permanent_assertion_2d.txt', 'r') as fin:
        line = fin.read()
    
    terms = line.strip().split(',')
    bl = []
    tr = []
    for i in range(dim):
        a, b = float(terms[i]), float(terms[dim + i])
        if b < a:
            a, b = b, a
        bl.append(a)
        tr.append(b)
    root_hc = Hypercube(dim, bl, tr)
    
    return root_hc, dim, train_list

def load_mixture_test_hypercube(input):
    test_list = []
    with open(input, "r") as fin:
        for line in fin.readlines():
            terms = line.strip().split(',')
            dim = (len(terms) - 1) // 2
            bl = []
            tr = []
            for i in range(dim):
                a, b = float(terms[i]), float(terms[dim + i])
                if b < a:
                    a, b = b, a
                bl.append(a)
                tr.append(b)
            hypercube = Hypercube(dim, bl, tr)
            test_list.append([hypercube, float(terms[len(terms) - 1])])
    return test_list

def load_hyperball(dataset, train_size, test_size):
    # input ball w./wo. card: q0, ..., q_{dim - 1}, r, p, sel
    if (dataset not in ball_query_filename) or (dataset not in ball_min_max_filename):
        print_error("unsupported dataset")
        sys.exit()
    cur_query_path = ball_query_path
    cur_query_filename = ball_query_filename[dataset]
    cur_min_max_path = ball_min_max_path
    cur_min_max_filename = ball_min_max_filename[dataset]

    whole_list = []
    with open(cur_query_path + cur_query_filename, 'r') as fin:
        for line in fin.readlines():
            terms = line.strip().split(',')
            dim = len(terms) - 3
            for i in range(dim):
                terms[i] = float(terms[i])
            q = HDPoint(dim, terms[:dim])
            r = float(terms[dim])
            p = math.floor(float(terms[dim + 1]))
            ball = Hyperball(dim, q, r, p)
            sel = float(terms[dim + 2])
            whole_list.append([ball, sel])
    if train_size + test_size > len(whole_list):
        print_error("deficient data size (%d)" % (len(whole_list)))
        sys.exit()

    train_list = whole_list[ : train_size]
    test_list = whole_list[-1 - test_size : -1]

    with open(cur_min_max_path + cur_min_max_filename, 'r') as fin:
        line = fin.read()
    
    terms = line.strip().split(',')
    bl = []
    tr = []
    for i in range(dim):
        a, b = float(terms[i]), float(terms[dim + i])
        if b < a:
            a, b = b, a
        bl.append(a)
        tr.append(b)
    root_hc = Hypercube(dim, bl, tr)

    return root_hc, dim, train_list, test_list

def load_hyperhalfspace(dataset, train_size, test_size):
    # input half-space w./wo. card : theta0, ..., theta_{dim - 1}, b, sel
    if (dataset not in halfspace_query_filename) or (dataset not in halfspace_min_max_filename):
        print_error("unsupported dataset")
        sys.exit()
    cur_query_path = halfspace_query_path
    cur_query_filename = halfspace_query_filename[dataset]
    cur_min_max_path = halfspace_min_max_path
    cur_min_max_filename = halfspace_min_max_filename[dataset]

    whole_list = []
    with open(cur_query_path + cur_query_filename, 'r') as fin:
        for line in fin.readlines():
            terms = line.strip().split(',')
            dim = len(terms) - 2
            for i in range(dim):
                terms[i] = float(terms[i])
            b = float(terms[dim])
            halfspace = Hyperhalfspace(dim, terms[:dim], b)
            sel = float(terms[dim + 1])
            whole_list.append([halfspace, sel])
    if train_size + test_size > len(whole_list):
        print_error("deficient data size (%d)" % (len(whole_list)))
        sys.exit()

    train_list = whole_list[ : train_size]
    test_list = whole_list[-1 - test_size : -1]

    with open(cur_min_max_path + cur_min_max_filename, 'r') as fin:
        line = fin.read()
    
    terms = line.strip().split(',')
    bl = []
    tr = []
    for i in range(dim):
        a, b = float(terms[i]), float(terms[dim + i])
        if b < a:
            a, b = b, a
        bl.append(a)
        tr.append(b)
    root_hc = Hypercube(dim, bl, tr)

    return root_hc, dim, train_list, test_list

def load_sample_data(dataset, size, attr_pointer):
    points, n_att = load_norm_table(dataset)
    sample_list = []
    count = 1
    length = len(points)
    mod = length // size
    for i in points:
        count += 1
        if count % mod == 1:
            i = i[:2]
            sample_list.append(i)
            if len(sample_list) == size:
                break
    return sample_list

def load_norm_table(table_name):
    print("Loading norm table %s..." % table_name)
    table = norm_tables[table_name]
    path = norm_data_path[table_name]
    tuples = np.loadtxt(path + table, delimiter=",", skiprows=0)
    print("%s's shape is " % table_name , tuples.shape)
    return tuples, tuples.shape[1]

def rectangle_intersection(rect1, rect2):
    x0 = max(rect1[0][0], rect2[0][0])
    y0 = max(rect1[0][1], rect2[0][1])
    x1 = min(rect1[1][0], rect2[1][0])
    y1 = min(rect1[1][1], rect2[1][1])
    return max(x1 - x0, 0) * max(y1 - y0, 0)

def write_data_to_csv(filename, array):
    print("Output to %s" % filename)
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        for i in range(0, len(array)):
            # for j in range(0, )
            # print(array[i])
            writer.writerow(array[i])

def store_mixture_results(output, result, header):
    with open(output, "w") as fout:
        writer = csv.writer(fout)
        writer.writerow(header)
        for i in range(len(result)):
            writer.writerow(result[i])

def write_nparray_to_csv(filename, tuple):
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        for i in range(0, tuple.shape[0]):
            writer.writerow(tuple[i])

def calc_q_error(est_result, pointers):
    q_error = []
    est_result.sort()
    # print("q-error: ", [round(est_result[pointer-1], 3) for pointer in pointers])
    for pointer in pointers:
        q_error.append(round(est_result[int(pointer) - 1], 6))
    return q_error

def sgn(x):
    return (x > epsilon) - (x < -epsilon)

def sgn2(a, b):
    return sgn(a - b)

def efficiency_test(model_filename, model):
    print("================ Efficiency Test ==================")
    model_path = "model/"
    print("Load model to %s" % (model_path + model_filename))
    with open(model_path + model_filename, "w") as fout:
        for i in range(len(model)):
            fout.write(",".join(str(val) for val in model[i]) + "\n")
        print("=============================================")

"""
def load_rect(dataset, train_size, test_size):
    # input data example: 0.011,0.511,-0.117,0.383,0.037465821
    if (dataset not in data_path) or (dataset not in query_filename) or (dataset not in min_max_filename):
        print_error("unsupported dataset")
        sys.exit()
    cur_data_path = data_path[dataset]
    cur_query_filename = query_filename[dataset]
    cur_min_max_filename = min_max_filename[dataset]

    whole_list = []
    with open(cur_data_path + cur_query_filename, 'r') as fin:
        for line in fin.readlines():
            whole_list.append(load_query(line.strip()))
    if train_size + test_size > len(whole_list):
        print_error("deficient data size (%d)" % (len(whole_list)))   
        sys.exit()

    # random.shuffle(whole_list)
    train_list = whole_list[ : train_size]
    test_list = whole_list[-1 - test_size : -1]
    
    with open(cur_data_path + cur_min_max_filename, 'r') as fin:
        line = fin.read()
    min_max_rect = load_range(line.strip())

    return min_max_rect, train_list, test_list

# We adjust the query by only taking its interaction with [0,1]^2. In practice, an outside rectangle will become a line where x/y = 0/1.
def load_query(line):
    terms = line.split(',')
    ncols = len(terms)    
    dim = (ncols - 1) // 2    

    for i in range(ncols):
        terms[i] = float(terms[i])
    for i in range(ncols - 1):
        terms[i] = min(max(terms[i], 0.0), 1.0) 
    sel = terms[ncols - 1]

    # We reorder the coordinates to get the bottom-left corner and the top-right corner.
    for i in range(dim):
        if terms[i * 2 + 1] < terms[i * 2]:
            terms[i * 2], terms[i * 2 + 1] = terms[i * 2 + 1], terms[i * 2]

    bl_corner = []
    tr_corner = []
    for i in range(dim):
        bl_corner.append(terms[i * 2])
        tr_corner.append(terms[i * 2 + 1])
    ret_query = [bl_corner, tr_corner, sel]
    return ret_query

# Similar to load_query()
def load_range(line):
    terms = line.split(',')
    ncols = len(terms)
    dim = ncols // 2

    for i in range(ncols):
        terms[i] = float(terms[i])
    for i in range(ncols):
        terms[i] = min(max(terms[i], 0.0), 1.0)

    for i in range(dim):
        if terms[i * 2 + 1] < terms[i * 2]:
            terms[i * 2], terms[i * 2 + 1] = terms[i * 2 + 1], terms[i * 2]

    bl_corner = []
    tr_corner = []
    for i in range(dim):
        bl_corner.append(terms[i * 2])
        tr_corner.append(terms[i * 2 + 1])
    
    ret_range = [bl_corner, tr_corner]

    return ret_range
"""