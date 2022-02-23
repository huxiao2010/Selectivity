import argparse
import sys
from utility import load_hyperhalfspace, print_error, write_data_to_csv
from half_space_estimator import HalfSpaceEstimator
from geometry import Line, Point

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='Forest-2d', help='[Forest-2d]')
# parser.add_argument('--train_size', type=int, default=1000, help='size of trainning set')
parser.add_argument('--split', type=str, default='rect', help='splitting method : [rect/poly]')
parser.add_argument('--test_size', type=int, default=100, help='size of test set')
parser.add_argument("--output_pre", type=str, default='', help='the prefix of the output filename; or do not output if empty')
args = parser.parse_args()

# Set of training size (input queries)
train_size_array = [50, 100, 200, 500, 1000]
# train_size_array = [100]
q_error_pointers = [49, 94, -2, -1]

if __name__ == "__main__":
    dataset = args.dataset
    # train_size = args.train_size
    split = args.split
    test_size = args.test_size
    output_pre = args.output_pre

    if (dataset not in ["Forest-2d"]):
        print_error("unsupported dataset")
        sys.exit()

    if (split not in ["rect", "poly"]):
        print_error("unsupported splitting method")
        sys.exit()

    if (test_size < 0):
        print_error("negative size")
        sys.exit()

    result_error = []
    result_time = []
    result_qerror = []

    print("=============================================")

    for train_size in train_size_array:
        _, dim, train_list, test_list = load_hyperhalfspace(dataset, train_size, test_size)
        min_max = [Line(Point(0.0, 0.0), Point(1.0, 0.0)), 
                   Line(Point(1.0, 0.0), Point(1.0, 1.0)),
                   Line(Point(1.0, 1.0), Point(0.0, 1.0)),
                   Line(Point(0.0, 1.0), Point(0.0, 0.0))]
        for i in range(len(train_list)):
            train_list[i][0] = train_list[i][0].toHalfspace()
        for i in range(len(test_list)):
            test_list[i][0] = test_list[i][0].toHalfspace()

        est = HalfSpaceEstimator(min_max, train_list)
        train_time, n_vars = est.train(split)

        print("Training Size: ", train_size)
        print("Training Time: %.3f(s)" % (train_time))
        error, q_error, eval_time = est.evaluate(test_list, q_error_pointers)
        print("Evaluation Time: %.3f(s)" % (eval_time))
        print("Test RMS Error: %.3f" % (error))
        print("Test Q Error: ", q_error)
        print("=============================================")

        result_error.append((train_size, error, n_vars))
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
