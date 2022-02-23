import argparse
import sys
from utility import load_hypercube, load_hyperball, load_hyperhalfspace, print_error, write_data_to_csv, efficiency_test
from hdpoint_estimator import HDPointEstimator

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='Power-2d',
                    help='[Power-(2,3,4,5,7)d/Forest-(2,3,4,5,8,10)d/Forest-(2,3,4,5,8,10)d-data]')
parser.add_argument('--query_type', type=str, default='rect', help='[rect/ball/halfspace]')
# parser.add_argument('--train_size', type=int, default=1000, help='size of trainning set')
parser.add_argument('--threshold', type=float, default=0.001, help='split threshold')
parser.add_argument('--buckets_limit', type=int, default=120000, help='the limited number of buckets')
parser.add_argument('--alpha', type=float, default=0.1, help='fraction of the uniform points in the whole 2d plane')
parser.add_argument('--test_size', type=int, default=100, help='size of test set')
parser.add_argument("--output_pre", type=str, default='',
                    help='the prefix of the output filename; or do not output if empty')
parser.add_argument("--eff_test", action="store_true", default=False, help='print model for efficiency test')
parser.add_argument("--solver", type=str, default='nnls', help='[nnls/cvxopt_linf]')
args = parser.parse_args()

# Set of training size (input queries)
train_size_array = [50, 200, 500, 1000, 2000]
# train_size_array = [2000, 3000, 4000, 5000, 6000, 9900]
q_error_pointers = [49, 94, -2, -1]

if __name__ == "__main__":
    dataset = args.dataset
    query_type = args.query_type
    # train_size = args.train_size
    threshold = args.threshold
    buckets_limit = args.buckets_limit
    alpha = args.alpha
    test_size = args.test_size
    output_pre = args.output_pre
    eff_test = args.eff_test
    solver = args.solver

    if (threshold < 0.0 or threshold > 1.0):
        print_error("unsupported stopping condition")
        sys.exit()

    if (alpha < 0.0 and alpha > 1.0):
        print_error("unsupported alpha")
        sys.exit()

    if (test_size < 0):
        print_error("negative size")
        sys.exit()

    if (solver not in ["nnls", "cvxopt_linf"]):
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

        est = HDPointEstimator(root_hc, train_list, dim, solver)
        train_time, n_vars = est.train(threshold, alpha, 4 * train_size, query_type)

        print("Training Size: ", train_size)
        print("Training Time: %.3f(s)" % (train_time))

        if eff_test:
            efficiency_test("hdpoint_%s_spl%f_a%f_tr%d_te%d.txt" % (dataset, threshold, alpha, train_size, test_size),
                            est.get_model())
            continue

        error, q_error, linf_error, eval_time = est.evaluate(test_list, query_type, q_error_pointers)
        print("Evaluation Time: %.3f(s)" % (eval_time))
        print("Test RMS Error: %.6f" % (error))
        print("Test L-INF Error: %.6f" % (linf_error))
        print("Test Q Error: ", q_error)
        print("=============================================")

        result_error.append((train_size, round(error, 5), n_vars))
        result_time.append((train_size, round(train_time, 3)))
        tmp = [train_size]
        for ii in q_error:
            tmp.append(ii)
        result_qerror.append(tuple(tmp))

    if len(output_pre) > 0:
        write_data_to_csv('../results/hdpoint/new/' + output_pre + '_rms_error.csv', result_error)
        write_data_to_csv('../results/hdpoint/new/' + output_pre + '_q_error.csv', result_qerror)
        write_data_to_csv('../results/hdpoint/new/' + output_pre + '_time.csv', result_time)
    else:
        print("No Output!")
