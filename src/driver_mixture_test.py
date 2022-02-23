from utility import load_mixture_train_hypercube, load_mixture_test_hypercube, store_mixture_results
from region_tree_estimator import RegionTreeEstimator

train_pos = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
# pos_to_char = {0.00 : "a", 0.25 : "b", 0.50 : "c", 0.75 : "d", 1.00 : "e"}
test_pos = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
train_size = [2000]
test_size = 100
q_error_pointers = [49, 94, -2, -1]
header = ["Train Data", "Est Name", "Train Position", "Train Size", "Test Position", "RMS Err", "QE-50th", "QE-95th", "QE-99th", "QE-100th"]

if __name__ == "__main__":
    ############## Currently, it only supports 2d mixture test ##############
    results = []
    
    for pos0 in train_pos:
        for size0 in train_size:
            print("==== Gaussian Mixture Test -- Dataset: %s -- Train Position: %.2f -- Train size: %d ====" % ("power-2d", pos0, size0))
            train_input_name = "../data/HighDim/gauss/power-gauss-2d-2100-s0.1-%.1f.txt" % pos0
            root_hc, dim, train_list = load_mixture_train_hypercube(train_input_name)
            train_list = train_list[:size0]
            buckets_limit = 4 * size0
            
            for threshold in [0.005]:   
                print("----- Train GOHist-spl%.4f-b%d -----" % (threshold, buckets_limit))
                est = RegionTreeEstimator(root_hc, train_list, dim)
                train_time, n_vars = est.train(buckets_limit, threshold)

                for pos1 in test_pos:
                    print("| Test Position: %.2f |" % pos1)
                    test_input_name = "../data/HighDim/gauss/power-gauss-2d-2100-s0.1-%.1f.txt" % pos1

                    test_list = load_mixture_test_hypercube(test_input_name)
                    test_list = test_list[-1 - test_size: -1]

                    error, q_error, eval_time = est.evaluate(test_list, q_error_pointers)
                    header = ["Train Data", "Train Position", "Train Size", "Test Position", "Est Name", "Training Time", "#Var", "RMS Err", "QE-50th", "QE-95th", "QE-99th", "QE-100th"]
                    result = ["power-2d", pos0, size0, pos1, "GOHist-spl%.3f-b%d" % (threshold, buckets_limit), train_time, n_vars, round(error, 6)] + q_error
                    results.append(result)

    output_name = "../results/Mixture/mixture_full.csv"
    results.sort()
    store_mixture_results(output_name, results, header)
            
