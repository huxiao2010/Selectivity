from utility import load_mixture_train_hypercube, load_mixture_test_hypercube, store_mixture_results
from region_tree_estimator import RegionTreeEstimator
from hdpoint_estimator import HDPointEstimator

data_path = "../data/Scalability/"
dataset = "Power-2d"
q_error_pointers = [49, 94, -2, -1]
header = ["Train Size", "Estimator", "Train Time", "#Vars", "RMS Err", "QE-50th", "QE-95th", "QE-99th", "QE-100th"]

if __name__ == "__main__":
    test_list = load_mixture_test_hypercube(data_path + "test_" + dataset + ".txt")
    results = []
    
    for num in range(5):
        root_hc, dim, train_list = load_mixture_train_hypercube(data_path + "train%d_" % (num) + dataset + ".txt")
        
        ### GOHist
        threshold = 0.003
        buckets_limit = 500000
        print("----- Start Test %d GOHist-spl%.3f-b%d -----" % (num, threshold, buckets_limit))

        est = RegionTreeEstimator(root_hc, train_list, dim)
        train_time, n_vars = est.train(buckets_limit, threshold)
        
        error, q_error, eval_time = est.evaluate(test_list, q_error_pointers)

        result = [2000, "GOHist-spl%.3f-b%d" % (threshold, buckets_limit), train_time, n_vars, round(error, 6)] + q_error
        results.append(result)
        ### PtsHist
        threshold = 0.04
        alpha = 0.1
        buckets_limit = 500000
        print("----- Start Test %d PTSHist-spl%.3f-a%.1f-b%d" % (num, threshold, alpha, buckets_limit))

        est = HDPointEstimator(root_hc, train_list, dim)
        train_time, n_vars = est.train(threshold, alpha, buckets_limit)

        error, q_error, eval_time = est.evaluate(test_list, "rect", q_error_pointers)

        result = [2000, "PtsHist-spl%.3f-a%.1f-b%d" % (threshold, alpha, buckets_limit), train_time, n_vars, round(error, 6)] + q_error
        results.append(result)

    output_name = "../results/Scalability/scalability_full.csv"
    results.sort()
    store_mixture_results(output_name, results, header)
            
