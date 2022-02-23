import argparse
import sys
from utility import load_rect, print_error, write_data_to_csv, efficiency_test
from rectangle_estimator import RectangleEstimator

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='Forest-2d', help='[Power-2d/Forest-2d/Forest-2d-data]')
parser.add_argument('--train_size', type=int, default=1000, help='size of trainning set')
parser.add_argument('--test_size', type=int, default=100, help='size of test set')
parser.add_argument('--sel_thres', type=str, default='0.0', help='[0.0, 1.0], optimization: only training queries >= sel_tres will be accepted')
parser.add_argument("--output_pre", type=str, default='', help='the prefix of the output filename; or do not output if empty')
parser.add_argument("--solver", type=str, default='nnls', help='[nnls/ridge/lasso/elastic/cvxopt_ls/cvxopt_mxen]')
parser.add_argument("--eff_test", action='store_true', default=False, help='print model for efficiency test')
args = parser.parse_args()

# Set of training size (input queries)
train_size_array = [50, 100, 200, 500]
q_error_pointers = [49, 94, -2, -1]

if __name__ == "__main__":
    dataset = args.dataset
    # train_size = args.train_size
    test_size = args.test_size
    sel_thres = float(args.sel_thres)    
    output_pre = args.output_pre
    solver = args.solver
    eff_test = args.eff_test


    if (test_size < 0):
        print_error("negative size")
        sys.exit()

    if (sel_thres < 0.0 or sel_thres > 1.0):
        print_error("wrong selectivity threshold")
        sys.exit()

    if (solver not in ["nnls", "ridge", "lasso", "elastic", "cvxopt_ls", "cvxopt_mxen"]):
        print_error("wrong solver")
        sys.exit()

    result_error = []
    result_time = []
    result_qerror = []

    print("=============================================")

    for train_size in train_size_array:
        min_max_rect, train_list, test_list = load_rect(dataset, train_size, test_size)
        min_max = min_max_rect + [1.000]
        
        est = RectangleEstimator(min_max, train_list, sel_thres, solver)
        train_time = est.train()

        print("Training Size: ", train_size)
        print("Training Time: %.3f(s)" % (train_time))

        if eff_test:
            efficiency_test("rect_%s_tr%d_te%d.txt" % (dataset, train_size, test_size), est.get_model())
            continue

        error, q_error, eval_time = est.evaluate(test_list, q_error_pointers)
        print("Evaluation Time: %.3f(s)" % (eval_time))
        print("Test RMS Error: %.3f" % (error))
        print("Test Q Error: ", q_error)
        print("=============================================")

        result_error.append((train_size, error))
        result_time.append((train_size, train_time))
        tmp = [train_size]
        for ii in q_error:
            tmp.append(ii)
        result_qerror.append(tuple(tmp))

    if len(output_pre) > 0:
        write_data_to_csv('../results/' + output_pre + '_rms_error.csv', result_error)
        write_data_to_csv('../results/' + output_pre + '_q_error.csv', result_qerror)
        write_data_to_csv('../results/' + output_pre + '_time.csv', result_time)
    else:
        print("No Output!")
