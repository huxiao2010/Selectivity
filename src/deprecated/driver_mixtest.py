from utility import load_mixture_hypercube, load_mixture_rect, load_rect, load_hypercube, store_mixture_results
from rectangle_estimator import RectangleEstimator
from hdpoint_estimator import HDPointEstimator
from region_tree_estimator import RegionTreeEstimator

mix_ratios = [0.00, 0.25, 0.50, 0.75, 1.00]
mix_train_size = [200, 500, 2000]
datasets = ["Forest-2d", "Forest-2d-data", "Power-2d", "Power-2d-data"]
q_error_pointers = [49, 94, -2, -1]
header = ["Train Data", "Est Name", "Train Size", "Test %R", "Test %D", "RMS Err", "QE-50th", "QE-95th", "QE-99th", "QE-100th"]

if __name__ == "__main__":
    results = []
    for dataset in datasets:
        for train_size in mix_train_size:
            if (train_size == 200):
                ##### GAHist #####
                print("----- Start GAHist -----")
                sel_thres = 0.0
                solver = "nnls"

                min_max_rect, train_list, _ = load_rect(dataset, train_size, 0)
                min_max = min_max_rect + [1.000]
                est = RectangleEstimator(min_max, train_list, sel_thres, solver)
                est.train()

                for ratio in mix_ratios:
                    test_name = dataset + "_r%.2f_d%.2f" % (ratio, 1 - ratio)
                    print(test_name)
                    input_name = "../data/Mixture/" + "-".join(dataset.split("-")[:2]) + "_r%.2f_d%.2f" % (ratio, 1 - ratio) + ".txt"   
                    test_list = load_mixture_rect(input_name)
                    error, q_error, eval_time = est.evaluate(test_list, q_error_pointers)
                    result = [dataset, "GAHist", train_size, ratio, 1 - ratio, round(error, 3)] + q_error
                    results.append(result)

            root_hc, dim, train_list, _ = load_hypercube(dataset, train_size, 0)

            ##### Pts #####
            print("----- Start Pts-spl0.1-a0.1 -----")
            threshold = 0.1
            alpha = 0.1
            query_type = "rect"

            est = HDPointEstimator(root_hc, train_list, dim)
            train_time, n_vars = est.train(threshold, alpha)


            for ratio in mix_ratios:
                test_name = dataset + "_r%.2f_d%.2f" % (ratio, 1 - ratio)
                print(test_name)
                input_name = "../data/Mixture/" + "-".join(dataset.split("-")[:2]) + "_r%.2f_d%.2f" % (ratio, 1 - ratio) + ".txt"   
                test_list = load_mixture_hypercube(input_name)
                error, q_error, eval_time = est.evaluate(test_list, query_type, q_error_pointers)
                result = [dataset, "Pts-spl0.1-a0.1", train_size, ratio, 1 - ratio, round(error, 3)] + q_error
                results.append(result)
                
            ##### GOHist #####
            for threshold in [0.1, 0.01, 0.001]:          
                buckets_limit = 500000
                print("----- Start GOHist-spl%.3f-b%d -----" % (threshold, buckets_limit))

                est = RegionTreeEstimator(root_hc, train_list, dim)
                train_time, n_vars = est.train(buckets_limit, threshold)

                for ratio in mix_ratios:
                    test_name = dataset + "_r%.2f_d%.2f" % (ratio, 1 - ratio)
                    print(test_name)                
                    input_name = "../data/Mixture/" + "-".join(dataset.split("-")[:2]) + "_r%.2f_d%.2f" % (ratio, 1 - ratio) + ".txt"   
                    test_list = load_mixture_hypercube(input_name)
                    error, q_error, eval_time = est.evaluate(test_list, q_error_pointers)
                    result = [dataset, "GOHist-spl%.3f-b%d" % (threshold, buckets_limit), train_size, ratio, 1 - ratio, round(error, 3)] + q_error
                    results.append(result)

    output_name = "../results/Mixture/mixture_full.csv"
    results.sort()
    store_mixture_results(output_name, results, header)
            
