import argparse
import time
import sys
import numpy as np
from utility import load_sample_data, load_rect, write_data_to_csv, load_halfspace, load_ball
from quad_tree import TreePoint, TreeNode, DensityTree, threshold, query_to_node, \
    sel_threshold, draw, build_quad_tree_by_half_space, build_quad_tree_by_rect, build_quad_tree_by_ball
from density_tree_estimator import DensityTreeEstimator
from matplotlib import gridspec


parser = argparse.ArgumentParser()
parser.add_argument('--type', type=str, default='rect', help='rect or hs or ball')
parser.add_argument('--dataset', type=str, default='Power', help='[DMV/Instacart/Power]')
parser.add_argument('--sample_size', type=int, default=1000, help='# of sampled data point')
parser.add_argument('--test_size', type=int, default=100, help='size of test set')
parser.add_argument("--solver", type=str, default='nnls', help='[nnls/ridge/lasso/elastic/cvxopt_ls/cvxopt_mxen]')
parser.add_argument("--output_pre", type=str, default='', help='the prefix of the output filename; or do not output if empty')
parser.add_argument("--by_density", action="store_true")
parser.add_argument("--by_data", action="store_true", help='Use sampled query(True) or data points(False)')


args = parser.parse_args()

# Some useful array to be changed in training
train_size_array = [1000]
q_error_pointers = [10, 20, 50, -1]

#
# DPI = 72
# np.random.seed(60)
#
# width, height = 600, 400
#
# N = 200
# coords = np.random.randn(N, 2) * height/3 + (width/2, height/2)
# points = [Point(*coord) for coord in coords]
#
# domain = Node(width/2, height/2, width, height, True)
# qtree = DensityTree(domain)
#
# for point in points:
#     qtree.insert(point)
#
# print('# of points in the domain =', qtree.cal_val())
# print('# of outside points = ', qtree.outside_points_num)
#
data_path_list = {'ball': '/ball/', 'hs': '/hf/', 'rect': '/rect/'}

def check_recursive_limit():
    max_recur = sys.getrecursionlimit()
    if max_recur < 10000:
        sys.setrecursionlimit(10000)
        print('WARNING: Set recursion limit from', max_recur, 'to', sys.getrecursionlimit())


if __name__ == "__main__":
    check_recursive_limit()
    dataset = args.dataset
    test_size = args.test_size
    solver = args.solver
    by_density = args.by_density
    by_data = args.by_data
    sample_size = args.sample_size  # sample the raw data points
    output_pre = args.output_pre
    wkld_type = args.type
    path = data_path_list[wkld_type]

    t1 = time.time()
    result_error = []
    result_time = []
    result_qerror = []
    result_depth = []
    result_tree = []

    for i in range(len(train_size_array)):
        sample_size = train_size_array[i]
        train_size = train_size_array[i]

        if wkld_type == 'hs':
            '''Use half space query to do selectivity estimation'''
            # min_max is the 4 lines of 1*1
            min_max, train_list, test_list = load_halfspace(dataset, sample_size, test_size)

            t2 = time.time()
            q_tree = build_quad_tree_by_half_space(train_list, min_max, pre_thres=1/20)
        elif wkld_type == 'ball':
            '''Use ball query to do selectivity estimation'''
            min_max, train_list, test_list = load_ball(dataset, train_size, test_size)
            t2 = time.time()
            q_tree = build_quad_tree_by_ball(train_list, pre_thres=1)
        else:
            '''Use rect query to do selectivity estimation'''
            min_max_rect, train_list, test_list = load_rect(dataset, sample_size, test_size)
            t2 = time.time()
            # train_list[0] = [[0, 0], [1, 1], 1]
            q_tree = build_quad_tree_by_rect(train_list)
        t3 = time.time()

        draw(q_tree, [], path)
        input()

        print("Build tree time: %.3f(s)" % (t3 - t2))
        print('# of sample size =', sample_size)
        print('# of MAX selectivity in one leaf =', sel_threshold)
        # print('# of points in the tree =', q_tree.cal_val())
        print('# of leaf nodes in the tree =', q_tree.cal_nodes(), len(q_tree.get_leaf_nodes()))
        print('# depth of the tree =', q_tree.cal_depth())

        if by_density:
            min_max_rect, train_list, test_list = load_rect(dataset, 0, test_size)
            estimator = DensityTreeEstimator(2, solver, [], test_list, q_tree)
            error, q_error = estimator.evaluate(q_error_pointers, by_density=True, wkld_type=wkld_type)
            print("Test RMS Error: %.3f" % error)
            print("Test Q Error: ", q_error)
            break
        else:
            estimator = DensityTreeEstimator(2, solver, train_list, test_list, q_tree)
            train_time = estimator.train(wkld_type)

            print("Training Size: ", train_size)
            print("=== Training Time: %.3f(s)" % train_time)
            print("=== Build + Train Time: %.3f(s)" % (train_time + t3 - t2))

            error, q_error, est_time_per_q = estimator.evaluate(
                q_error_pointers, by_density=False, wkld_type=wkld_type)

            print("Test RMS Error: %.3f" % error)
            print("Test Q Error: ", q_error)
            print("=============================================")

            result_error.append((train_size, round(error, 3)))
            result_time.append((train_size, round(train_time + (t3 - t2), 3), est_time_per_q))
            result_tree.append((train_size, q_tree.cal_nodes(), q_tree.cal_depth()))
            tmp = [train_size]
            for ii in q_error:
                tmp.append(ii)
            result_qerror.append(tuple(tmp))

    if len(output_pre) > 0:
        write_data_to_csv('../results/density_results/' + path + output_pre + '_rms_error.csv', result_error)
        write_data_to_csv('../results/density_results/' + path + output_pre + '_q_error.csv', result_qerror)
        write_data_to_csv('../results/density_results/' + path + output_pre + '_time.csv', result_time)
        write_data_to_csv('../results/density_results/' + path + output_pre + '_tree.csv', result_tree)
    else:
        print("No Output!")
