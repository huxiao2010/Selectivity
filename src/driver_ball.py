import argparse
import sys
from utility import load_hyperball, print_error, write_data_to_csv
from ball_estimator import BallEstimator

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, default='Forest-2d', help='[Forest-2d]')
# parser.add_argument('--train_size', type=int, default=1000, help='size of trainning set')
parser.add_argument('--nsplits', type=int, default=2, help='number of splits obtained from in each dimension')
#parser.add_argument('--split', type=str, default='unif', help='split method : [unif/density]')
parser.add_argument('--test_size', type=int, default=100, help='size of test set')
parser.add_argument("--output_pre", type=str, default='', help='the prefix of the output filename; or do not output if empty')
args = parser.parse_args()

# Set of training size (input queries)
# train_size_array = [10, 20, 50, 100, 200, 500]
train_size_array = [50, 100, 200]
q_error_pointers = [49, 94, -2, -1]

if __name__ == "__main__":
    dataset = args.dataset
    # train_size = args.train_size
    nsplits = args.nsplits
    #split = args.split
    test_size = args.test_size
    output_pre = args.output_pre

    if (dataset not in ["Forest-2d"]):
        print_error("unsupported dataset")
        sys.exit()

    if (nsplits < 2):
        print_error("unsupported number of splits")
        sys.exit()

    # if (split not in ["unif", "density"]):
    #     print_error("unsupported split method")

    if (test_size < 0):
        print_error("negative size")
        sys.exit()

    result_error = []
    result_time = []
    result_qerror = []

    print("=============================================")

    for train_size in train_size_array:
        min_max, dim, train_list, test_list = load_hyperball(dataset, train_size, test_size)
        min_max = [min_max.bl, min_max.tr]
        for i in range(len(train_list)):
            train_list[i][0] = train_list[i][0].toBall()
        for i in range(len(test_list)):
            test_list[i][0] = test_list[i][0].toBall()

        est = BallEstimator(min_max, train_list)
        train_time, n_vars = est.train(nsplits)

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
        write_data_to_csv('../results/ball/' + output_pre + '_rms_error.csv', result_error)
        write_data_to_csv('../results/ball/' + output_pre + '_q_error.csv', result_qerror)
        write_data_to_csv('../results/ball/' + output_pre + '_time.csv', result_time)
    else:
        print("No Output!")
