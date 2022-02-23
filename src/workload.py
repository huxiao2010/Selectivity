import numpy as np
import random
from sklearn import preprocessing
from tqdm import tqdm

np.set_printoptions(suppress=True)
OPS = {
    '>': np.greater,
    '<': np.less,
    '>=': np.greater_equal,
    '<=': np.less_equal,
    '=': np.equal,
    # '[]': in_between
}

data_path = {'DMV': '../tables/dmv/', 'Instacart': '../tables/Instacart/', 'Power': '../tables/power/',
             'Forest': '../tables/forest10/', 'DMV-2': "../tables/dmv/", 'Census': "../tables/census13/",
             'Census-2': "../tables/census13/"}
norm_data_path = {'DMV': '../tables/norm/dmv/',
                  'Instacart': '../tables/norm/Instacart/',
                  'Power': '../tables/norm/power/',
                  'Forest': '../tables/norm/forest/'}

tables = {'DMV': "dmv.csv", 'Power': "power.csv", 'Forest': 'forest.csv', 'DMV-2': "DMV-new.csv",
          'Census': "census.csv", 'Census-2': "Census-new.csv"}
# csv Upper Letter means Norm
norm_tables = {'DMV': "Dmv.csv", 'Power': "Power.csv", 'Forest': 'Forest.csv'}


def load_table(table_name):
    table = tables[table_name]
    path = data_path[table_name]
    rows = []
    print("Begin Loading %s..." % table_name)
    with open(path + table, 'r') as table_file:
        first_line = table_file.readline().strip()
        attr = first_line.split(",")
        for line in table_file.readlines():
            line = line.strip().split(',')
            line = [str(i) for i in line]
            rows.append(line)
    tuples = np.array(rows)
    print("Load %s succeed!" % table_name)
    print(table_name, "'s shape is ", tuples.shape)
    return tuples, attr

def sample_table(table_name):
    table = tables[table_name]
    path = data_path[table_name]
    rows = []
    print("Begin Loading %s..." % table_name)
    with open(path + table, 'r') as table_file:
        head_line = table_file.readline()
        lines = table_file.readlines()
        random.shuffle(lines)
        lines = lines[:-1]
        table_file.close()
    for line in lines:
        line = line.strip().split(',')
        line = [str(i).strip() for i in line]
        rows.append(line)
    tuples = np.array(rows)
    print("Load sampled %s succeed!" % table_name)
    print(table_name, "'s shape is ", tuples.shape)
    np.savetxt(path + table_name + '-new.csv', tuples, delimiter=",", fmt='%s')
    return tuples

def stat_table(table_name, attr):
    table = tables[table_name]
    path = data_path[table_name]
    print("Begin Loading %s..." % table_name)
    tuples = np.loadtxt(path + table, delimiter=',', dtype=str)
    print(table_name, "'s shape is ", tuples.shape)

    dicts = []
    for i in attr:
        dict_i = {}
        for t_i in tuples:
            if t_i[i] in dict_i.keys():
                dict_i[t_i[i]] = dict_i[t_i[i]] + 1
            else:
                dict_i[t_i[i]] = 1
        dicts.append(dict_i)
        print(dict_i)

    # Generate data-driven workload
    # First, norm dict
    dict_list = []
    for d in range(len(dicts)):
        dict_list_i = []
        old_key_i = list(dicts[d])
        dict_list_i.append(old_key_i)
        key_i = list(dicts[d])
        val_i = list(dicts[d].values())
        n = len(dicts[d])
        for i in range(n):
            key_i[i] = round(i / n, 3)
        dict_list_i.append(key_i)
        dict_list_i.append(val_i)
        dict_list.append(dict_list_i)
    # Second, gen workload from data
    tuples_new = tuples.copy()
    np.random.shuffle(tuples_new)
    total = len(tuples_new)
    wkld = []
    for i_n in tqdm(range(2100)):
        query = []
        for i in range(len(attr)):
            it = tuples_new[i_n][attr[i]]
            name_ = dict_list[i][0]
            key_ = dict_list[i][1]
            index = name_.index(it)
            # print(it, index)
            center = key_[index]
            # print(center)
            a = round(random.random(), 3) * 0.5
            query.append(max(round(center - a * 0.5, 3), 0))
            query.append(min(round(center + a * 0.5, 3), 1))
        sel = 0

        for t_i in range(len(tuples)):
            label = 1
            for i in range(len(attr)):
                # print(dict_list[i])
                name_ = dict_list[i][0]
                key_ = dict_list[i][1]
                index = name_.index(tuples[t_i][attr[i]])
                norm_val = key_[index]
                if query[i * 2] > norm_val or norm_val > query[i * 2 + 1]:
                    label = 0
            if label == 1:
                sel += 1
        query.append(sel/total)
        # print(query)
        wkld.append(query)
    workload = np.asarray(wkld)
    np.savetxt("../data/workload/data_sensitive/census" + '-data-2100.txt', workload, delimiter=",", fmt='%s')




# Norm all of the attributes to (0, 1)
def norm_table(tuples, table_name):
    min_max_norm = preprocessing.MinMaxScaler()
    tuples = min_max_norm.fit_transform(tuples)
    print(tuples.shape)
    print("Normalize succeed!")
    path = norm_data_path[table_name]
    print("Begin writing %s ..." % table_name)
    # write_nparray_to_csv(path + table_name+'.csv', tuples)
    np.savetxt(path + table_name+'.csv', tuples, delimiter=",", fmt='%s')
    print("Write succeed!")
    return tuples


def load_norm_table(table_name):
    print("Loading norm table %s" % table_name)
    table = norm_tables[table_name]
    path = norm_data_path[table_name]
    tuples = np.loadtxt(path + table, delimiter=",", skiprows=0)
    print("%s's shape is " % table_name , tuples.shape)
    return tuples, tuples.shape[1]


def norm(tuples):
    for col in range(tuples.shape[1]):
        for i in range(tuples.shape[0]):
            tmp = tuples[:, col]
            tmp = tmp.flatten()
            _min = np.min(tmp)
            _max = np.max(tmp)
            tuples[i][col] = float(i - _min) / (_max - _min)
    return tuples


def write_sampled_data(tuples, num, name):
    random.shuffle(tuples)
    tuples = tuples[:num]
    workload = np.asarray(tuples)
    np.savetxt("../data/workload/" + name + "-data-"
               + str(len(workload)) + ".txt", workload, delimiter=",", fmt='%s')

def gen_workload_from_data(tuples, name, d, attr_pointers):
    path = '../data/workload/power-data-10000.txt'
    output_list = []

    with open(path, 'r') as file:
        k = 0
        for line in tqdm(file.readlines()):
            # if k > 2100:
            #     break
            k += 1
            line = line.strip().split(',')
            query = []
            for i in range(d):
                a = round(random.random(), 3)
                query.append(max(round(float(line[attr_pointers[i]]) - 0.5 * a, 3), 0))
                query.append(min(round(float(line[attr_pointers[i]]) + 0.5 * a, 3), 1))
            count = search(tuples, attr_pointers, query)
            sel = round(count / tuples.shape[0], 9)
            # print(count, sel)
            query.append(sel)
            output_list.append(query)
    workload = np.asarray(output_list)
    np.savetxt("../data/workload/data_sensitive/" + name, workload, delimiter=",", fmt='%s')


def gen_workload_from_gauss(tuples, name, d, attr_pointers, num):
    output_list = []

    for num_i in tqdm(range(num)):
        q = []
        for d_i in range(d):
            val = round(random.gauss(0.6, 0.1/3), 3)
            a = round(random.random(), 3)
            q.append(min(max(round(val - 0.25 * a, 3), 0), 1))
            q.append(max(min(round(val + 0.25 * a, 3), 1), 0))
        count = search(tuples, attr_pointers, q)
        sel = round(count / tuples.shape[0], 9)
        q.append(sel)
        # print(q)
        output_list.append(q)
    workload = np.asarray(output_list)
    np.savetxt("../data/workload/" + name, workload, delimiter=",", fmt='%s')


def gen_pure_gauss(name, d, num):
    output_list = []

    for num_i in tqdm(range(num)):
        q = []

        for d_i in range(d):
            val = round(random.gauss(0.5, 0.167), 3)
            a = round(random.random(), 3)
            q.append(max(round(val - 0.25 * a, 3), 0))
            q.append(min(round(val + 0.25 * a, 3), 1))
        # print(q)
        output_list.append(q)
    workload = np.asarray(output_list)
    np.savetxt("../data/workload/" + name, workload, delimiter=",", fmt='%s')


def gen_range_queries(num, d):
    ret = []
    for i in range(num):
        tmp = []
        for i in range(d):
            a, b = get_two_random()
            tmp.extend([a, b])
        ret.append(tmp)
    return ret


def get_two_random():
    a = round(random.random(), 3)
    b = round(random.random(), 3)
    return min(a, b), max(a, b)


# attr_pointers is a list to point which attributes will be queried
# [1, 3] means column 2 and column 4 will be queried
def gen_range_workload(tuples, num, attr_pointers):
    print("Begin generating range workload...")
    query_arr = gen_range_queries(num, len(attr_pointers))
    wkld = []
    for i in tqdm(query_arr):
        count = search(tuples, attr_pointers, i)
        sel = round(count/tuples.shape[0], 9)
        i.append(sel)
        wkld.append(i)
    return wkld

# e.g. generate 4d workload based on 3d
def gen_series_range_workload(tuples, num, attr_pointers):
    print("Generate 3d - 5d workload together")
    query_arr = gen_range_queries(num, 3)
    for att in range(len(attr_pointers) - 3):
        wkld = []
        for i in tqdm(query_arr):
            count = search(tuples, attr_pointers, i)
            sel = round(count / tuples.shape[0], 9)
            i.append(sel)
            wkld.append(i)
            workload = np.asarray(wkld)
            np.savetxt("../data/workload/forest-series-" + str(3 + att) + "d-"
                       + str(len(workload)) + ".txt", wkld, delimiter=",", fmt='%s')


###
# Input: 1 all the tuples, 2 num of queries you want, 3 on which attributes
# Output: wkld [x1, y1, r, sel]
# random center (x1, x2) inside [1 * 1], random radius [0, 2^0.5]
# round = 3
###
def gen_ball_workload(tuples, num, attr_pointers):
    print("Begin generating ball workload...")
    wkld = []
    total = tuples.shape[0]

    for i in tqdm(range(num)):
        c_x = round(random.random(), 3)
        c_y = round(random.random(), 3)
        r = round(random.uniform(0, 1.4), 3)
        count = ball_search(tuples, attr_pointers, c_x, c_y, r)
        sel = round(count / total, 5)
        wkld.append([c_x, c_y, r, sel])
        # print([c_x, c_y, r, sel])
    return wkld

###
# Generate ball query on high dimensional space
def gen_ball_workload_highd(tuples, num, attr_pointers):
    print("Begin generating ball workload on high d...")
    wkld = []
    d = len(attr_pointers)
    p = 2  # norm
    for i in tqdm(range(num)):
        # initial random list
        random_list = []
        for d_i in range(d):
            random_list.append(round(random.random(), 3))
        r = round(random.random() * pow(d, 1/p), 3)
        random_list.append(r)
        random_list.append(p)
        count = 0
        for t in tuples:
            val = 0
            for d_i in range(d):
                val += pow(t[d_i] - random_list[d_i], p)
            val = pow(val, 1/p)
            if val <= r:
                count += 1
        sel = round(count / tuples.shape[0], 5)
        random_list.append(sel)
        # print(random_list)
        wkld.append(random_list)
    return wkld


def gen_ball_workload_from_data_highd(tuples, num, attr_pointers, name):
    print("Begin generating ball workload on high d...")
    output_list = []
    d = len(attr_pointers)
    p = 2  # norm
    path = '../data/workload/forest-data-10000.txt'
    size = tuples.shape[0]
    with open(path, 'r') as file:
        k = 0
        for line in tqdm(file.readlines()):
            if k > num:
                break
            k += 1
            line = line.strip().split(',')
            random_list = []
            val = 0
            for d_i in range(d):
                q_i = round(random.random(), 3)
                random_list.append(q_i)
                val += pow(float(line[d_i]) - q_i, p)
            r = pow(val, 1/p)
            random_list.append(r)
            count = 0
            for t in tuples:
                val = 0
                for d_i in range(d):
                    val += pow(t[d_i] - random_list[d_i], p)
                val = pow(val, 1/p)
                # print val
                if val <= r:
                    count += 1

            sel = round(count / size, 9)
            random_list.append(p)
            random_list.append(sel)
            # print(count, sel)
            output_list.append(random_list)
            # print(random_list)
    workload = np.asarray(output_list)
    np.savetxt("../data/workload/data_sensitive/ball/" + name, workload, delimiter=",", fmt='%s')



###
# Input: 1 all the tuples, 2 num of queries you want, 3 on which attributes
# Output: wkld [x1, y1, x2, y2, sel]
# direction: from lower to higher
# right hand rule
# round = 3
###
def gen_hspace_workload(tuples, num, attr_pointers):
    print("Begin generating half space workload...")
    # Every edge has a slack, we have 6 case to choose two edges and split the {(0,0) to (1,1)} square
    # Assume the square has a, b, c, d
    wkld = []
    for i in tqdm(range(num)):
        pointer_ = i % 6
        slack_a = round(random.random(), 3)
        slack_b = round(random.random(), 3)
        if slack_b == slack_a:
            slack_b = round(random.random(), 3)
        k, b = 0, 0
        x1, y1, x2, y2 = 0, 0, 0, 0
        if pointer_ == 0:
            # first case: 1, 2; we have (0, slack_a), (slack_b, 0)
            x1, y1, x2, y2 = 0, slack_a, slack_b, 0
        if pointer_ == 1:
            # second case: 1, 3; we have (0, slack_a), (1, slack_b)
            x1, y1, x2, y2 = 0, slack_a, 1, slack_b
        if pointer_ == 2:
            # Third case: 1, 4; we have (0, slack_a), (slack_b, 1)
            x1, y1, x2, y2 = 0, slack_a, slack_b, 1
        if pointer_ == 3:
            # 4th case: 2, 3; we have (slack_a, 0), (1, slack_b)
            x1, y1, x2, y2 = slack_a, 0, 1, slack_b
        if pointer_ == 4:
            # 5th case: 2, 4; we have (slack_a, 0), (slack_b, 1)
            x1, y1, x2, y2 = slack_a, 0, slack_b, 1
        if pointer_ == 5:
            # 6th case: 3, 4; we have (1, slack_a), (slack_b, 1)
            x1, y1, x2, y2 = 1, slack_a, slack_b, 1
        else:
            assert "wrong"

        if x1 - x2 == 0:
            p = 0.0001
        else:
            p = x1 - x2

        k = round((y1 - y2) / p, 3)
        b = round((y2 * x1 - y1 * x2) / p, 3)
        # linear scan query, calculate selectivity
        count = hspace_search(tuples, attr_pointers, k, b)
        sel = round(count/tuples.shape[0], 5)

        # 从低点到高点的右手
        if y1 < y2:
            if x1 > x2:
                wkld.append([x1, y1, x2, y2, 1 - sel])
            else:
                wkld.append([x1, y1, x2, y2, sel])
        else:
            if x1 > x2:
                wkld.append([x1, y1, x2, y2, 1 - sel])
            else:
                wkld.append([x1, y1, x2, y2, sel])
    print(len(wkld))
    # print(wkld)
    return wkld


def gen_hspace_workload_highd(tuples, num, attr_pointers):
    print("Begin generating half space workload on high d...")
    d = len(attr_pointers)
    wkld = []

    max_val = 0
    for tuple in tuples:
        tmp = 0
        for d_i in range(d):
            tmp += tuple[d_i]
        if tmp > max_val:
            max_val = tmp

    for i in tqdm(range(num)):
        random_list = []
        for i in range(d):
            random_list.append(round(random.uniform(-1.0, 1.0), 3))
        if [i for i in random_list if i > 0]:
            random_list.append(round(random.uniform(0.0, 1.0), 3))
        elif [i for i in random_list if i < 0]:
            random_list.append(round(random.uniform(-1.0, 0.0), 3))
        else:
            random_list.append(round(random.uniform(-1.0, 1.0), 3))
        count = 0
        for tuple in tuples:
            val = 0
            for d_i in range(d):
                val += random_list[d_i] * tuple[d_i]
            if val > round(random_list[-1] * max_val, 3):
                count += 1
        sel = round(count / tuples.shape[0], 5)
        random_list[-1] = round(random_list[-1] * max_val, 3)
        random_list.append(sel)
        # print(random_list)
        wkld.append(random_list)
    print(len(wkld))
    return wkld

def gen_hspace_workload_from_data_highd(tuples, num, attr_pointers, name):
    print("Begin generating half space workload on high d...")
    d = len(attr_pointers)
    output_list = []
    path = '../data/workload/forest-data-10000.txt'
    size = tuples.shape[0]
    with open(path, 'r') as file:
        k = 0
        for line in tqdm(file.readlines()):
            if k > num:
                break
            k += 1
            line = line.strip().split(',')
            random_list = []
            val = 0
            for d_i in range(d):
                theta_i = round(random.uniform(-1.0, 1.0), 3)
                random_list.append(theta_i)
                val += theta_i * float(line[d_i])
            b = round(val, 3)
            count = 0
            for tuple in tuples:
                val = 0
                for d_i in range(d):
                    val += random_list[d_i] * tuple[d_i]
                if val > b:
                    count += 1
            sel = round(count / tuples.shape[0], 5)
            random_list.append(b)
            random_list.append(sel)
            output_list.append(random_list)
            # print(random_list)
    workload = np.asarray(output_list)
    np.savetxt("../data/workload/data_sensitive/halfspace/" + name, workload, delimiter=",", fmt='%s')


def search(tuples, attr_pointers, query):
    count = 0
    d = len(attr_pointers)
    if len(query) != 2 * d:
        assert "Wrong"

    for t in range(tuples.shape[0]):
        row = tuples[t]
        flag = 1
        for i in range(d):
            item = row[attr_pointers[i]]
            if query[2 * i] > item or query[2 * i + 1] < item:
                flag = 0
        if flag == 1:
            count += 1
    return count


def ball_search(tuples, attr_pointers, x, y, r):
    count = 0
    for t in range(tuples.shape[0]):
        row = tuples[t]
        if pow(pow((x - row[attr_pointers[0]]), 2) + pow((y - row[attr_pointers[0]]), 2), 0.5) <= r:
            count += 1
    return count


def hspace_search(tuples, attr_pointers, k, b):
    # half space query may have two cardinality
    count = 0
    # count_down = 0
    for t in range(tuples.shape[0]):
        row = tuples[t]
        item_1 = row[attr_pointers[0]]
        item_2 = row[attr_pointers[1]]
        if item_2 - item_1 * k > b:
            count += 1
    return count


def change_wkld_order(file_name, d):
    path = '../data/workload/data_sensitive/'
    output_list = []
    with open(path + file_name, 'r') as file:
        for line in tqdm(file.readlines()):
            line = line.strip().split(',')
            tmp_1 = []
            tmp_2 = []
            for i in range(2 * d):
                if i % 2 == 0:
                    tmp_1.append(line[i])
                else:
                    tmp_2.append(line[i])
            output_list.append(tmp_1 + tmp_2 + [line[-1]])
    output_list = np.asarray(output_list)
    np.savetxt('../data/HighDim/' + file_name, output_list, delimiter=',', fmt='%s')


def change_back(file_name, d):
    path = '../data/HighDim/'
    path_2 = '../data/changeback/'
    output_list = []
    with open(path + file_name, 'r') as file:
        for line in tqdm(file.readlines()):
            line = line.strip().split(',')
            tmp = []
            for i in range(d):
                tmp.append(line[i])
                tmp.append(line[i + d])
            tmp.append(line[-1])
            output_list.append(tmp)
    output_list = np.asarray(output_list)
    np.savetxt(path_2 + file_name, output_list, delimiter=',', fmt='%s')



# t, att = load_table('Forest')
# t = norm_table(t, 'Forest')


# n_t, n_att = load_norm_table('Forest')
# _attr_pointers = [0, 1, 2, 3, 4, 5]
# 3, 4, 5, 6, 7, 8, 9
# workload = gen_range_workload(tuples=n_t, num=11000, attr_pointers=_attr_pointers)
# # workload = gen_hspace_workload(tuples=n_t, num=2000, attr_pointers=[0, 1])
# # workload = gen_ball_workload(tuples=n_t, num=2000, attr_pointers=[0, 1])

# workload = np.asarray(workload)
# np.savetxt("../data/workload/power-" + str(len(_attr_pointers)) + "d-"
#            + str(len(workload)) + ".txt", workload, delimiter=",", fmt='%s')



# write_sampled_data(n_t, 10000, 'forest')
# n_t, n_att = load_norm_table('Power')
# _attr_pointers = [0, 1]

# write_sampled_data(n_t, 10000, 'power')


# change_back('assertion_forest_2d.txt', 2)

# 生成多个10000的power 2d
# gen_workload_from_data(n_t, 'power-data-100000-2d-5.txt', 2, _attr_pointers)
# change_wkld_order('power-data-100000-2d-5.txt', 2)

# 生成高维data-aware的forest
# gen_ball_workload_from_data_highd(n_t, 2100, _attr_pointers, 'forest-data-' + str(len(_attr_pointers)) + "d-2100.txt")
# gen_hspace_workload_from_data_highd(n_t, 2100, _attr_pointers, 'forest-data-' + str(len(_attr_pointers)) + "d-2100.txt")

# workload = gen_hspace_workload_highd(n_t, 2100, _attr_pointers)
# workload = gen_ball_workload_highd(n_t, 2100, _attr_pointers)
# workload = np.asarray(workload)
# np.savetxt("../data/HighDim/Halfspace/forest-" + str(len(_attr_pointers)) + "d-"
#            + str(len(workload)) + ".txt", workload, delimiter=",", fmt='%s')


# gen_workload_from_gauss(n_t, 'gauss/power-gauss-2d-2100-s0.1-r0.5-0.6.txt', 2, _attr_pointers, 2100)

# change_wkld_order('gauss/power-gauss-2d-2100-s0.1-r0.25-0.6.txt', 2)
# change_wkld_order('gauss/power-gauss-2d-2100-s0.1-r0.25-0.7.txt', 2)
# change_wkld_order('gauss/power-gauss-2d-2100-s0.1-r0.25-0.5.txt', 2)
# change_wkld_order('gauss/power-gauss-2d-2100-s0.1-r0.5-0.6.txt', 2)
# change_wkld_order('gauss/power-gauss-2d-2100-s0.1-r0.5-0.7.txt', 2)


# gen_pure_gauss('gauss/pure-gauss-1000-2d-2.txt', 2, 1000)

# sample_table('DMV')
# stat_table('DMV-2', [3, 6])  # address and date
# sample_table('Census')
# stat_table('Census-2', [1, 2])  # age and job
# change_wkld_order('census-data-2100-2d.txt', 2)
change_wkld_order('dmv-data-2100-2d.txt', 2)

