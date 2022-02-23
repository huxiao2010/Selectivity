from utility import load_mixture_train_hypercube, load_mixture_test_hypercube, store_mixture_results
from hdpoint_estimator import HDPointEstimator
from region_tree_estimator import RegionTreeEstimator

mix_ratios = [0.00, 0.25, 0.50, 0.75, 1.00]
mix_train_size = [2000]
datasets = ["Forest-2d", "Power-2d"]
q_error_pointers = [49, 94, -2, -1]
header = ["Train Data", "Est Name", "Train Size", "Train (R/Train size)%", "Test (R/Test size)%", "RMS Err", "QE-50th", "QE-95th", "QE-99th", "QE-100th"]

def check(l1, l2):
    for i in range(5):
        if l1[i] != l2[i]:
            return False
    return True

if __name__ == "__main__":
    ############## Currently, it only supports 2d mixture test ##############
    results = []
    for num in range(10):
        result_id = 0
        for train_size in mix_train_size:
            for dataset in datasets:
                for train_ratio in mix_ratios:
                    print("==== Mixture Test: %d -- Train size: %d -- Dataset: %s -- Train ratio: %.2f ====" % (num, train_size, dataset, train_ratio))
                    train_input_name = "../data/Mixture/train/train%d_" % (num) + dataset + "_tr%d_r%.2f_d%.2f" % (train_size, train_ratio, 1 - train_ratio) + ".txt"
                    print(train_input_name)
                    root_hc, dim, train_list = load_mixture_train_hypercube(train_input_name)
                    ##### Pts #####
                    print("----- Start Pts-spl0.1-a0.1 -----")
                    threshold = 0.1
                    alpha = 0.1
                    query_type = "rect"

                    est = HDPointEstimator(root_hc, train_list, dim)
                    train_time, n_vars = est.train(threshold, alpha)

                    for test_ratio in mix_ratios:
                        test_name = dataset + "_r%.2f_d%.2f" % (test_ratio, 1 - test_ratio)
                        test_input_name = "../data/Mixture/test/test%d_" % (num) + dataset + "_r%.2f_d%.2f" % (test_ratio, 1 - test_ratio) + ".txt"   
                        test_list = load_mixture_test_hypercube(test_input_name)
                        print(test_name)
                        error, q_error, eval_time = est.evaluate(test_list, query_type, q_error_pointers)
                        result = [dataset, "Pts-spl0.1-a0.1", train_size, train_ratio, test_ratio, round(error, 6)] + q_error
                        if len(results) <= result_id:
                            results.append(result)
                        elif check(results[result_id], result):
                            for i in range(5, 10):
                                results[result_id][i] += result[i]
                        else:
                            assert True
                        result_id += 1
                    ##### GOHist #####
                    for threshold in [0.1, 0.01, 0.001]:   
                        buckets_limit = 500000
                        print("----- Start GOHist-spl%.3f-b%d -----" % (threshold, buckets_limit))

                        est = RegionTreeEstimator(root_hc, train_list, dim)
                        train_time, n_vars = est.train(buckets_limit, threshold)

                        for test_ratio in mix_ratios:
                            test_name = dataset + "_r%.2f_d%.2f" % (test_ratio, 1 - test_ratio)
                            print(test_name)          
                            test_input_name = "../data/Mixture/test/test%d_" % (num) + dataset + "_r%.2f_d%.2f" % (test_ratio, 1 - test_ratio) + ".txt"   
                            test_list = load_mixture_test_hypercube(test_input_name)
                            error, q_error, eval_time = est.evaluate(test_list, q_error_pointers)
                            result = [dataset, "GOHist-spl%.3f-b%d" % (threshold, buckets_limit), train_size, train_ratio, test_ratio, round(error, 6)] + q_error
                            if len(results) <= result_id:
                                results.append(result)
                            elif check(results[result_id], result):
                                for i in range(5, 10):
                                    results[result_id][i] += result[i]
                            else:
                                assert True
                            result_id += 1

    output_name = "../results/Mixture/mixture_full.csv"
    for i in range(len(results)):
        for j in range(5, 10):
            results[i][j] *= 0.1
    results.sort()
    store_mixture_results(output_name, results, header)
            
