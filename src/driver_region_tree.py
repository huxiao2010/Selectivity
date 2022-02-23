import argparse
import sys
from utility import efficiency_test, load_hypercube, load_hyperball, load_hyperhalfspace, print_error, write_data_to_csv
from region_tree_estimator import RegionTreeEstimator

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='Power-2d-data', help='[Power-(2,3,4,5,7)d/Forest-(2,3,4,6,8,10)d/Forest-(2,3,4,6,8,10)d-data]')
parser.add_argument('--query_type', type=str, default='rect', help='[rect/ball/halfspace]')
# parser.add_argument('--train_size', type=int, default=1000, help='size of trainning set')
parser.add_argument('--threshold', type=float, default=0.004, help='split threshold')
parser.add_argument('--buckets_limit', type=int, default=1000000, help='the limited number of buckets')
parser.add_argument('--test_size', type=int, default=100, help='size of test set')
parser.add_argument("--output_pre", type=str, default='', help='the prefix of the output filename; or do not output if empty')
parser.add_argument("--eff_test", action='store_true', default=False, help='print model for efficiency test')
parser.add_argument("--solver", type=str, default='nnls', help='[nnls/cvxopt_linf/gurobi_linf/cplex_linf]')
args = parser.parse_args()

# Set of training size (input queries)
train_size_array = [50, 200, 500, 1000, 2000]

# train_size_array = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 9900]
# train_size_array = [2000]
q_error_pointers = [49, 94, -2, -1]

if __name__ == "__main__":
    dataset = args.dataset
    query_type = args.query_type
    # train_size = args.train_size
    threshold = args.threshold
    buckets_limit = args.buckets_limit
    test_size = args.test_size
    output_pre = args.output_pre
    eff_test = args.eff_test
    solver = args.solver

    if (query_type != "rect" and dataset.split("-")[1] != "2d"):
        print_error("error: region_tree estimator only supports 2d-ball and 2d-halfspace queries")
        sys.exit()

    if (threshold < 0):
        print_error("unsupported threshold")
        sys.exit()

    if (buckets_limit < 0):
        print_error("unsupported buckets_limit")
        sys.exit()

    if (test_size < 0):
        print_error("negative size")
        sys.exit()

    if (solver not in ["nnls", "cvxopt_linf", "gurobi_linf", "cplex_linf"]):
        print_error("unsupported solver")
        sys.exit()

    result_error = []
    result_time = []
    result_qerror = []

    print("=============================================")

    for train_size in train_size_array:
        if query_type == "rect":
            root_hc, dim, train_list, test_list = load_hypercube(dataset, train_size, test_size)
        elif query_type == "ball":
            root_hc, dim, train_list, test_list = load_hyperball(dataset, train_size, test_size)
        elif query_type == "halfspace":
            root_hc, dim, train_list, test_list = load_hyperhalfspace(dataset, train_size, test_size)
        
        est = RegionTreeEstimator(root_hc, train_list, dim, solver)
        train_times, n_vars = est.train(4 * train_size, threshold)

        print("Training Size: ", train_size)
        print("Training Time: %.3f(s)" % (train_times))

        if eff_test:
            efficiency_test("region-tree_%s_spl%f_b%d_tr%d_te%d.txt" % (dataset, threshold, buckets_limit, train_size, test_size), est.get_model())
            continue

        error, q_error, linf_error, eval_time = est.evaluate(test_list, q_error_pointers)
        print("Evaluation Time: %.3f(s)" % (eval_time))
        print("Test RMS Error: %.6f" % (error))
        print("Test L-INF Error: %.6f" % (linf_error))
        print("Test Q Error: ", q_error)
        print("=============================================")

        result_error.append((train_size, round(error, 6), n_vars))
        result_time.append((train_size,
                            round(train_times, 3)))
        tmp = [train_size]
        for ii in q_error:
            tmp.append(ii)
        result_qerror.append(tuple(tmp))


    if len(output_pre) > 0:
        write_data_to_csv('../results/highd/new/' + output_pre + '_rms_error.csv', result_error)
        write_data_to_csv('../results/highd/new/' + output_pre + '_q_error.csv', result_qerror)
        write_data_to_csv('../results/highd/new/' + output_pre + '_time.csv', result_time)
    else:
        print("No Output!")
