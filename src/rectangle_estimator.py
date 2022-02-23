import time
import math
import numpy as np
from scipy.optimize import nnls
from utility import rectangle_intersection, calc_q_error, sgn2
from sklearn.linear_model import ElasticNet, Ridge
from cvxopt import matrix, solvers, spdiag, log

class RectangleEstimator:
    def __init__(self, min_max, train_list, threshold, solver):
        self.min_max = min_max
        self.train_list = train_list
        self.threshold = threshold
        self.solver = solver

        self.n = len(train_list) # number of queries
        self.qn = 0 # number of qualified queries
        self.dim = 2
        self._lines = [[], []]
        self._cnt = [0, 0]
        self._density = []
        self._train_error = 0.0
        self._qualified_queries = []

    def _cover_bucketes(self, query):
        # query = [[x0, x1], [y0, y1], card]
        # res = [[x_lb, x_ub], [y_lb, y_ub]]
        res = []
        for dim in range(self.dim):
            query_lb = query[0][dim]
            query_ub = query[1][dim]

            lb = 0
            ub = len(self._lines[dim]) - 1
            # lower bound
            le = 0
            ri = len(self._lines[dim]) - 1
            while le <= ri:
                mid = (le + ri) // 2
                if sgn2(self._lines[dim][mid], query_lb) != 1: # <=
                    lb = mid
                    le = mid + 1
                else:
                    ri = mid - 1
            # upper bound
            le = 0
            ri = len(self._lines[dim]) - 1
            while le <= ri:
                mid = (le + ri) // 2
                if sgn2(self._lines[dim][mid], query_ub) != -1: # >=
                    ub = mid
                    ri = mid - 1
                else:
                    le = mid + 1
            res.append([lb, ub])
        return res
            

    def train(self):
        start_time = time.time()
        print("Number of queries : %d" % (self.n))
        for i in range(self.n):
            if self.train_list[i][2] >= self.threshold:
                self._qualified_queries.append(self.train_list[i])
        self.qn = len(self._qualified_queries)
        print("Number of qualified queries : %d" % (self.qn))
        time_0 = time.time()
        print("Filter Time: %.3f" % (time_0 - start_time))

        ori_lines = [[], []]
        ori_cnt = [0, 0]
        for i in range(self.dim):
            cur_lines = [(self.min_max[0][i], -1), (self.min_max[1][i], -1)]
            for j in range(self.qn):
                cur_lines.append((self._qualified_queries[j][0][i], j))
                cur_lines.append((self._qualified_queries[j][1][i], j))
            cur_lines.sort(key=lambda x:x[0])

            ori_lines[i].append(cur_lines[0])
            ori_cnt[i] += 1
            for j in range(1, len(cur_lines)):
                ori_lines[i].append(cur_lines[j])
                ori_cnt[i] += 1

        x = 0
        self._lines[0] = []
        self._cnt[0] = 0
        while x < ori_cnt[0] - 1 and sgn2(ori_lines[0][x][0], self.min_max[1][0]) == -1:
            val_0, _ = ori_lines[0][x]
            while x + 1 < ori_cnt[0] - 1 and sgn2(val_0, ori_lines[0][x + 1][0]) == 0:
                x += 1
            self._lines[0].append(val_0)
            self._cnt[0] += 1
            x += 1
        
        y = 0
        self._lines[1] = []
        self._cnt[1] = 0
        while y < ori_cnt[1] - 1 and sgn2(ori_lines[1][y][0], self.min_max[1][1]) == -1:
            val_1, _ = ori_lines[1][y]
            while y + 1 < ori_cnt[1] - 1 and sgn2(val_1, ori_lines[1][y + 1][0]) == 0:
                y += 1
            self._lines[1].append(val_1)
            self._cnt[1] += 1
            y += 1

        self._lines[0].append(1.0)
        self._lines[1].append(1.0)   

        involved_vars = []
        for i in range(self.qn):
            cover_range = self._cover_bucketes(self._qualified_queries[i])
            involved_vars.append([])
            for x in range(cover_range[0][0], cover_range[0][1]):
                for y in range(cover_range[1][0], cover_range[1][1]):
                    involved_vars[i].append((x, y))

        area = []
        for i in range(len(self._lines[0]) - 1):
            for j in range(len(self._lines[1]) - 1):
                area.append((self._lines[0][i + 1] - self._lines[0][i]) * (self._lines[1][j + 1] - self._lines[1][j]))

        time_1 = time.time()
        print("Plane Split Time: %.3f" % (time_1 - time_0))

        n_var = self._cnt[0] * self._cnt[1]
        print("Number of Variables: %d" % (n_var))
        A = []
        b = []
        for i in range(self.qn):
            A.append([0.0] * n_var)
            for (x, y) in involved_vars[i]:
                A[i][y * self._cnt[0] + x] = 1.0
            b.append(self._qualified_queries[i][2])
        A.append([1.0] * n_var)
        b.append(1.0)

        A = np.array(A)
        b = np.array(b)
        if self.solver == "nnls":
            A = np.row_stack((A, np.array([1e-3] * n_var)))
            b = np.append(b, 0.0)
            x, self._train_error = nnls(A, b)
        elif self.solver == "ridge":
            solver = Ridge(fit_intercept=False, alpha=1.0)
            solver.fit(A, b)
            x = solver.coef_
            print("Ridge Original Training Error: %.3f" % np.sum(np.square(A.dot(x) - b)))
            self._train_error = np.sum(np.square(A.dot(x) - b))
        elif self.solver == 'elastic':
            solver = ElasticNet(fit_intercept=False, alpha=1.0, l1_ratio=1e-6)
            solver.fit(A, b)
            x = solver.coef_
            print("ElasticNet Original Training Error: %.3f" % np.sum(np.square(A.dot(x) - b)))
            self._train_error = np.sum(np.square(A.dot(x) - b))
        elif self.solver == 'lasso':
            solver = ElasticNet(fit_intercept=False, alpha=1.0)
            solver.fit(A, b)
            x = solver.coef_
            print("Lasso Original Training Error: %.3f" % np.sum(np.square(A.dot(x) - b)))
            self._train_error = np.sum(np.square(A.dot(x) - b))
        elif self.solver == 'cvxopt_ls':
            A = matrix(A)
            b = matrix(b) 
            I = matrix(0.0, (n_var, n_var))
            I[::n_var+1] = 1.0
            G = matrix([-I])
            h = matrix([0.0] * n_var)
            x = solvers.coneqp(A.T*A, -A.T*b, G, h)['x']
        elif self.solver == 'cvxopt_mxen':
            G = matrix(0.0, (n_var, n_var))
            G[::n_var+1] = -1.0
            h = matrix(0.0, (n_var, 1))
            
            AA = A.copy()
            bb = b.copy() 

            AA = matrix(AA)
            bb = matrix(bb)
            def F(x=None, z=None):
                if x is None: return 0, matrix(1.0, (n_var, 1))
                if min(x) <= 0: return None
                f = x.T*log(x) 
                grad = 1.0 + log(x)
                if z is None: return f, grad.T
                H = spdiag(z[0] * x**-1)
                return f, grad.T, H
            sol = solvers.cp(F, G, h, A=AA, b=bb)
            x = sol['x']

        time_2 = time.time()
        print("Equation Construction and Solving Time: %.3f" % (time_2 - time_1))

        # x = post_opt(A, b, x)

        """layers = {} # layer_hash -> [total_density, total_area / size]
        for i in range(n_var):
            val = hash(tuple(A[:, i]))
            if val not in layers:
                layers[val] = [0.0, 0.0]
            layers[val][0] += x[i]
            layers[val][1] += area[i]
            # layers[val][1] += 1.0"""
        for i in range(n_var):
            # val = hash(tuple(A[:, i]))
            # self._density.append(layers[val][0] / layers[val][1] * area[i])
            # self._density.append(layers[val][0] / layers[val][1])
            self._density.append(x[i])
        """time_3 = time.time()
        print("Reassignment Time: %.3f" % (time_3 - time_2))"""

        print("Training error: %.3f" % (self._train_error))
        end_time = time.time()
        return end_time - start_time
    
    def get_model(self):
        model = []
        for x in range(self._cnt[0]):
            for y in range(self._cnt[1]):
                id = y * self._cnt[0] + x
                model.append([self._lines[0][x], self._lines[1][y], self._lines[0][x + 1], self._lines[1][y + 1], self._density[id]])
        return model

    def evaluate(self, test_list, pointers):
        start_time = time.time()
        error = 0.0
        test_len = len(test_list)
        est_result = []

        for i in range(test_len):
            sel = test_list[i][2]
            est_sel = 0.0
            cover_range = self._cover_bucketes(test_list[i])
            for x in range(cover_range[0][0], cover_range[0][1]):
                for y in range(cover_range[1][0], cover_range[1][1]):
                    area = (self._lines[0][x + 1] - self._lines[0][x]) * (self._lines[1][y + 1] - self._lines[1][y])
                    d = self._density[y * self._cnt[0] + x]
                    intersection_area = rectangle_intersection(test_list[i][:2], [[self._lines[0][x], self._lines[1][y]], [self._lines[0][x + 1], self._lines[1][y + 1]]])
                    # assert d >= 0, "WRONG: d < 0"
                    est_sel += d / area * intersection_area
            
            # if est_sel >= 1.0 or est_sel <= 0.0:
            #     bad_test_count += 1
            #     est_sel = max(0.0 + epsilon, min(1.0 - epsilon, est_sel))
            est_sel = min(1.000, max(est_sel, 0.000))

            error += (sel - est_sel) ** 2
            q_error = math.inf
            if est_sel == 0 or sel == 0:
                q_error = 1.000
            elif min(est_sel, sel) > 0:
                q_error = max(est_sel, sel) / min(est_sel, sel)
            # est_sel += 1
            # sel += 1
            # q_error = max(est_sel, sel) / min(est_sel, sel)
            
            est_result.append(q_error)
        
        rms = (error / test_len) ** 0.5
        ret_qerror = calc_q_error(est_result, pointers)
        return rms, ret_qerror, time.time() - start_time

def post_opt(A, b, x, iters=50):
    _x = x.copy()
    _d = A.dot(x) - b
    _A_square_sum = A.copy()
    for i in range(_A_square_sum.shape[0]):
        for j in range(_A_square_sum.shape[1]):
            _A_square_sum[i][j] = _A_square_sum[i][j] ** 2
    _A_square_sum = np.asarray(_A_square_sum.sum(axis=0)).ravel()
    min_loss = np.sum(np.square(_d))
    print("Loss before post-opt : %.6f" % min_loss)
    for j in range(iters):
        for i in range(A.shape[1]):
            _k = A[:, i]
            _k_nonzero = _k > 0
            delta = -0.5 * np.sum(_d[_k_nonzero] * _k[_k_nonzero]) / _A_square_sum[i]
            if _x[i] + delta >= 0.0 and _x[i] + delta <= 1.0:
                _x[i] += delta
                _d[_k_nonzero] += _k[_k_nonzero] * delta

        cur_loss = np.sum(np.square(_d))
        if min_loss > cur_loss:
            min_loss = cur_loss
        else:
            break
    print("Loss after post-opt : %.6f" % min_loss)
    return _x
