import time
import math
import sys
from matplotlib.pyplot import new_figure_manager
import numpy as np
from utility import calc_q_error
from geometry import HDPoint, Hyperball, Hypercube, Hyperhalfspace, hdPointInHypercube, hyperCubeIntersectionArea, sgn
from scipy.optimize import nnls

max_iter = 100000000

class WeightedHDPoint:
    def __init__(self, hdp, w):
        self.hdp = hdp
        self.w = w

class KDTreeNode:
    def __init__(self, parent, depth, dim):
        self.parent = parent
        self.depth = depth
        self.dim = dim
        self.ranges = []
        
        self.sum = self.le = self.ri = None
    def updateChildren(self, le, ri):
        self.le, self.ri = le, ri
        self.sum = le.getSum() + ri.getSum()
        for i in range(self.dim):
            self.ranges.append([min(le.ranges[i][0], ri.ranges[i][0]), max(le.ranges[i][1], ri.ranges[i][1])])

    def getSum(self):
        return self.sum
    def updateLeaf(self, w, ranges):
        self.sum = w
        self.ranges = ranges
    def estimate(self, object):
        if self.le == None or self.ri == None:
            x = []
            for i in range(self.dim):
                x.append(self.ranges[i][0])
            hdp = HDPoint(self.dim, x)
            if object.inside(hdp):
                return self.sum
            else:
                return 0.0

        bl = []
        tr = []
        for i in range(self.dim):
            bl.append(self.ranges[i][0])
            tr.append(self.ranges[i][1])
        hc = Hypercube(self.dim, bl, tr)

        if isinstance(object, Hypercube):
            area = hyperCubeIntersectionArea(hc, object)
            if sgn(area) == 0:
                return 0.0
            elif sgn(area - hc.area) == 0:
                return self.sum

            return self.le.estimate(object) + self.ri.estimate(object)
        elif isinstance(object, Hyperball):
            cnt = 0
            for i in range(1 << self.dim):
                x = []
                for j in range(self.dim):
                    if i & (1 << j) == (1 << j):
                        x.append(hc.tr[j])
                    else:
                        x.append(hc.bl[j])
                hdp = HDPoint(self.dim, x)
                if object.inside(hdp):
                    cnt += 1
                else:
                    cnt -= 1
            if cnt == (1 << self.dim):
                return self.sum

            area = hyperCubeIntersectionArea(hc, object._hc)
            if cnt == -(1 << self.dim) and sgn(area) == 0:
                return 0.0
            
            return self.le.estimate(object) + self.ri.estimate(object)
        elif isinstance(object, Hyperhalfspace):
            cnt = 0
            for i in range(1 << self.dim):
                x = []
                for j in range(self.dim):
                    if i & (1 << j) == (1 << j):
                        x.append(hc.tr[j])
                    else:
                        x.append(hc.bl[j])
                hdp = HDPoint(self.dim, x)
                if object.inside(hdp):
                    cnt += 1
                else:
                    cnt -= 1
            if cnt == (1 << self.dim):
                return self.sum
            if cnt == -(1 << self.dim):
                return 0.0
            
            return self.le.estimate(object) + self.ri.estimate(object)
        else:
            sys.exit()
        
class HDPointEstimator:
    def __init__(self, root_hc, train_list, dim, solver):
        self.root_hc = root_hc
        self.train_list = train_list
        self.dim = dim
        # each line is [hc, cardinality]
        self.solver = solver

        self.n = len(train_list)
        self._card = []
        self._train_error = 0.0
        self._n_var = 0
        self._kd_tree_root = None
        self._hdps = []

    def _build_kd_tree(self, whdps, split_dim, dim, parent, depth):
        cur = KDTreeNode(parent, depth, dim)
        whdps.sort(key = lambda tmp: tmp.hdp.x[split_dim])
        if len(whdps) > 1:
            mid = len(whdps) >> 1
            le = self._build_kd_tree(whdps[:mid], (split_dim + 1) % dim, dim, cur, depth + 1)
            ri = self._build_kd_tree(whdps[mid:], (split_dim + 1) % dim, dim, cur, depth + 1)
            cur.updateChildren(le, ri)
        else:
            ranges = []
            for i in range(dim):
                ranges.append([whdps[0].hdp.x[i]] * 2)
            cur.updateLeaf(whdps[0].w, ranges)
        return cur

    def train(self, threshold, alpha, buckets_limit, query_type):
        start_time = time.time()
        print("Number of Queries : %d" % (self.n))

        total_sel = 0.0
        for i in range(self.n):
            total_sel += self.train_list[i][1]
 
        hdps = []
        num_a = min(round(buckets_limit * alpha), buckets_limit - len(hdps))
        hdps.extend(self.root_hc.sample(num_a))

        for i in range(self.n):
            num_a = min(round(self.train_list[i][1] / total_sel * buckets_limit * (1 - alpha)), buckets_limit - len(hdps))
            hdps.extend(self.train_list[i][0].sample(num_a))

        self._hdps = hdps
        self._n_var = len(hdps)

        print("Number of Variables : %d" % (self._n_var))
        time_0 = time.time()
        print("Plane Split Time : %.3f" % (time_0 - start_time))

        if self.solver == "nnls":
            A = []
            b = []
            for i in range(self.n):
                A.append([0.0] * self._n_var)
                for j in range(self._n_var):
                    if self.train_list[i][0].inside(hdps[j]):
                        A[i][j] = 1.0
                b.append(self.train_list[i][1])
            A.append([1.0] * self._n_var)
            b.append(1.0)

            time_1 = time.time()
            print("Equation Construction Time : %.3f" % (time_1 - time_0))

            A = np.array(A)
            b = np.array(b)
            x, self._train_error = nnls(A, b, max_iter)
            time_2 = time.time()
            print("Equation Solving Time : %.3f" % (time_2 - time_1))
        elif self.solver == "cvxopt_linf":
            c = []
            for j in range(self._n_var):
                c.append(0.0)
            c.append(1.0)
            G = []
            h = []
            for j in range(self._n_var):
                G.append([])
                for i in range(self.n):
                    if self.train_list[i][0].inside(hdps[j]):
                        G[j].append(-1.)
                        G[j].append(1.)
                    else:
                        G[j].append(0.)
                        G[j].append(0.)
            G.append([])
            for i in range(self.n):
                G[self._n_var].append(-1.)
                h.append(-self.train_list[i][1])
                G[self._n_var].append(-1.)
                h.append(self.train_list[i][1])
            for j in range(self._n_var):
                for k in range(self._n_var + 1):
                    if j == k:
                        G[k].append(-1.)
                    else:
                        G[k].append(0.)
                h.append(0.)
            A = []
            for j in range(self._n_var):
                A.append([1.0])
            A.append([0.0])
            b = [1.0]

            c = matrix(c)
            G = matrix(G)
            h = matrix(h)
            A = matrix(A)
            b = matrix(b)
            time_1 = time.time()
            print("Equation Construction Time : %.3f" % (time_1 - time_0))

            x = solvers.lp(c, G, h, A, b)['x']
            time_2 = time.time()
            print("Equation Solving Time : %.3f" % (time_2 - time_1))
        

        for i in range(self._n_var):
            self._card.append(x[i])
        
        # # !!!!!!!!!!!!!!!! Just for drawing figure !!!!!!!!!!!!!!!!!!!!
        # print("!!!!!!! Draw figure !!!!!!! [Please delete this part]")
        # with open("hdps_spl%f_a%f_tr%d.txt" % (threshold, alpha, len(self.train_list)), "w") as fout:
        #     for i in range(len(self._hdps)):
        #         for j in range(self.dim - 1):
        #                 fout.write(str(self._hdps[i].x[j]) + ",")
        #         fout.write(str(self._hdps[i].x[self.dim - 1]) + ",")
        #         fout.write(str(self._card[i]) + "\n")
        # # !!!!!!!!!!!!!!!! Just for drawing figure !!!!!!!!!!!!!!!!!!!!

        whdps = []
        for i in range(self._n_var):
            whdps.append(WeightedHDPoint(hdps[i], self._card[i]))
        self._kd_tree_root = self._build_kd_tree(whdps, 0, self.dim, None, 0)
        time_3 = time.time()
        print("KD Tree Construction Time : %.3f" % (time_3 - time_2))

        time_4 = time.time()
        rms_error = 0.0
        linf_error = 0.0
        for i in range(self.n):
            sel = self.train_list[i][1]
            if query_type == 'rect':
                est_sel = self._kd_tree_root.estimate(self.train_list[i][0])
            else:
                est_sel = 0.0
                for j in range(self._n_var):
                    if self.train_list[i][0].inside(self._hdps[j]):
                        est_sel += self._card[j]
                est_sel = min(1.000, max(est_sel, 0.000))
                rms_error += (sel - est_sell) ** 2
                linf_error = max(linf_error, abs(sel - est_sel))
        rms_error = (rms_error / self.n) ** 0.5
        print("Training RMS Error : %.6f" % (rms_error))
        print("Training LInf Error : %.6f" % (linf_error))
        return time_4 - start_time, self._n_var

    def get_model(self):
        model = []
        l = [self._kd_tree_root]
        pos = 0
        while pos < len(l):
            cur = l[pos]
            bl = []
            tr = []
            for i in range(cur.dim):
                bl.append(cur.ranges[i][0])
                tr.append(cur.ranges[i][1])
            le = -1
            ri = -1
            if cur.le != None:
                l.append(cur.le)
                le = len(l) - 1
            if cur.ri != None:
                l.append(cur.ri)
                ri = len(l) - 1
            model.append(bl + tr + [cur.sum, le, ri])
            pos += 1
        return model

    def evaluate(self, test_list, query_type, pointers):
        start_time = time.time()
        error = 0.0
        linf_error = 0.0
        test_len = len(test_list)
        est_result = []

        for i in range(len(test_list)):
            sel = test_list[i][1]
            
            if query_type == 'rect':
                est_sel = self._kd_tree_root.estimate(test_list[i][0])
            else:
                est_sel = 0.0
                for j in range(self._n_var):
                    if test_list[i][0].inside(self._hdps[j]):
                        est_sel += self._card[j]

            # if est_sel >= 1.0 or est_sel <= 0.0:
            #     bad_test_count += 1
            #     est_sel = max(0.0 + epsilon, min(1.0 - epsilon, est_sel))
            est_sel = min(1.000, max(est_sel, 0.000))

            error += (sel - est_sel) ** 2
            linf_error = max(linf_error, abs(sel - est_sel))
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
        return rms, ret_qerror, linf_error, time.time() - start_time
