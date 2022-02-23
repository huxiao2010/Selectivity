import time
import math
import numpy as np
from utility import calc_q_error
from geometry import Hypercube
from scipy.optimize import nnls
from cvxopt import matrix, solvers
import cplex
import gurobipy

epsilon = 0.001

class RegionTree:
    def __init__(self, root_hc, buckets_limit):
        self.buckets_limit = buckets_limit       

        self.nnode = 1
        self.nleaves = 1
        self.height = 1 # depth is in [0, height)
        self.root = TreeNode(root_hc, 0)
        
        self.nodes = [self.root]
    def addNodes(self, hcs, depth):
        if self.nleaves - 1 + len(hcs) > self.buckets_limit:
            return False, []
        self.nleaves = self.nleaves - 1 + len(hcs)
        if depth + 1 > self.height:
            self.height = depth + 1
        ids = []
        for i in range(len(hcs)):
            self.nodes.append(TreeNode(hcs[i], depth))
            ids.append(self.nnode)
            self.nnode += 1
        return True, ids
    def hypercubesOfLeaves(self):
        hcs = []
        for i in range(self.nnode):
            if len(self.nodes[i].child) > 0:
                continue
            hcs.append(self.nodes[i].hc)
        return hcs

class TreeNode:
    def __init__(self, hc, depth):
        self.hc = hc
        self.child = []
        self.depth = depth
    def est_card(self, object, card):
        if object.area == 0.0:
            return 0.0
        return object.intersectionAreaWithHypercube(self.hc) / object.area * card
    def split(self, tree, dim):
        if len(self.child) == 1 << dim:
            return True
        hcs = []
        for i in range(1 << dim):
            bl = []
            tr = []
            for j in range(dim):
                le, ri = self.hc.bl[j], self.hc.tr[j]
                mid = (le + ri) / 2
                if i & (1 << j) == (1 << j):
                    bl.append(mid)
                    tr.append(ri)
                else:
                    bl.append(le)
                    tr.append(mid)
            hcs.append(Hypercube(dim, bl, tr))
        flag, self.child = tree.addNodes(hcs, self.depth + 1) 
        return flag

class RegionTreeEstimator:
    def __init__(self, root_hc, train_list, dim, solver):
        self.root_hc = root_hc
        self.train_list = train_list
        self.dim = dim
        self.solver = solver
        # each line is [geometric object, cardinality]

        self.n = len(train_list)
        self._card = []
        self._train_error = 0.0
        self._n_var = 0
        self._hcs = []

    def _recursiveSplit(self, object, card, tree, node, threshold):
        if node.est_card(object, card) > threshold:
            if node.split(tree, self.dim):
                for i in range(len(node.child)):
                    if not self._recursiveSplit(object, card, tree, tree.nodes[node.child[i]], threshold):
                        return False
            else:
                return False
        return True

    def train(self, buckets_limit, split_threshold):
        start_time = time.time()
        print("Number of Queries : %d" % (self.n))

        region_tree = RegionTree(self.root_hc, buckets_limit)
        for i in range(self.n):
            if not self._recursiveSplit(self.train_list[i][0], self.train_list[i][1], region_tree, region_tree.root, split_threshold):
                break
        
        # for i in range(region_tree.nnode):
        #     if len(region_tree.nodes[i].child) > 0:
        #         flag = False
        #         for j in range(self.n):
        #             if region_tree.nodes[i].est_card(self.train_list[j][0], self.train_list[j][1]) >= split_threshold:
        #                 flag = True
        #                 break
        #         if not flag:
        #             print("%d should not be splitted" % i)
        #     else:
        #         flag = True
        #         for j in range(self.n):
        #             if region_tree.nodes[i].est_card(self.train_list[j][0], self.train_list[j][1]) >= split_threshold:
        #                 flag = False
        #                 break
        #         if not flag:
        #             print("%d should be splitted" % i)
        
        self._hcs = region_tree.hypercubesOfLeaves()
        self._n_var = len(self._hcs)

        print("Number of Variables : %d" % (self._n_var))
        time_0 = time.time()
        print("Plane Split Time : %.3f" % (time_0 - start_time))
            
        if self.solver == "nnls":
            A = []
            b = []
            for i in range(self.n):
                A.append([0.0] * self._n_var)
                for j in range(self._n_var):
                    int_area = self.train_list[i][0].intersectionAreaWithHypercube(self._hcs[j])
                    A[i][j] = int_area / self._hcs[j].area
                b.append(self.train_list[i][1])
            A.append([1.0] * self._n_var)
            b.append(1.0)

            time_1 = time.time()
            print("Equation Construction Time : %.3f" % (time_1 - time_0))

            A = np.array(A)
            b = np.array(b)
            x, self._train_error = nnls(A, b)
                
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
                    int_area = self.train_list[i][0].intersectionAreaWithHypercube(self._hcs[j])
                    G[j].append(-int_area / self._hcs[j].area)
                    G[j].append(int_area / self._hcs[j].area)
            G.append([])
            for i in range(self.n):
                G[self._n_var].append(-1.0)
                h.append(-self.train_list[i][1])
                G[self._n_var].append(-1.0)
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
        elif self.solver == "gurobi_linf":
            c = []
            for j in range(self._n_var):
                c.append(0.0)
            c.append(1.0)
            G = []
            h = []
            for i in range(self.n):
                G.append([])
                for j in range(self._n_var):
                    int_area = self.train_list[i][0].intersectionAreaWithHypercube(self._hcs[j])
                    G[i * 2].append(-int_area / self._hcs[j].area)
                G[i * 2].append(-1.)
                h.append(-self.train_list[i][1])
                G.append([])
                for j in range(self._n_var):
                    int_area = self.train_list[i][0].intersectionAreaWithHypercube(self._hcs[j])
                    G[i * 2 + 1].append(int_area / self._hcs[j].area)
                G[i * 2 + 1].append(-1.)
                h.append(self.train_list[i][1])
            for j in range(self._n_var):
                G.append([])
                for k in range(self._n_var + 1):
                    if j == k:
                        G[self.n * 2 + j].append(-1.)
                    else:
                        G[self.n * 2 + j].append(0.)
                h.append(0.)
            A = [[]]
            for j in range(self._n_var):
                A[0].append(1.)
            A[0].append(0.)
            b = [1.]

            model = gurobipy.Model("gurobi_linf")
            x = model.addVars(self._n_var + 1, lb = 0., ub = 1., name = 'x')
            model.update()
            model.setObjective(x.prod(c), gurobipy.GRB.MINIMIZE)
            lenG = len(G)
            model.addConstrs(x.prod(G[i]) <= h[i] for i in range(lenG))
            model.addConstr(x.prod(A[0]) == b[0])
            model.optimize()
            x = []
            for v in model.getVars():
                x.append(v.x)
        elif self.solver == "cplex_linf":
            prob = cplex.Cplex()
            prob.objective.set_sense(prob.objective.sense.minimize)
            obj = []
            for j in range(self._n_var):
                obj.append(0.0)
            obj.append(1.0)
            lbs = [0.0] * (self._n_var + 1)
            ubs = [1.0] * (self._n_var + 1)
            prob.variables.add(obj = obj, lb = lbs, ub = ubs)

            G = []
            h = []
            senses = []

            for i in range(self.n):
                constraint = [[], []]
                for j in range(self._n_var):
                    constraint[0].append(j)
                    int_area = self.train_list[i][0].intersectionAreaWithHypercube(self._hcs[j])
                    constraint[1].append(int_area / self._hcs[j].area)
                constraint[0].append(self._n_var)
                constraint[1].append(-1.)
                G.append(constraint)
                h.append(self.train_list[i][1])
                senses.append("L")

                constraint = [[], []]
                for j in range(self._n_var):
                    constraint[0].append(j)
                    int_area = self.train_list[i][0].intersectionAreaWithHypercube(self._hcs[j])
                    constraint[1].append(-int_area / self._hcs[j].area)
                constraint[0].append(self._n_var)
                constraint[1].append(-1.)
                G.append(constraint)
                h.append(-self.train_list[i][1])
                senses.append("L")
            
            constraint = [[], []]
            for j in range(self._n_var):
                constraint[0].append(j)
                constraint[1].append(1.)
            G.append(constraint)
            h.append(1.)
            senses.append("E")

            for j in range(self._n_var):
                constraint = [[j], [1.]]
                G.append(constraint)
                h.append(0.)
                senses.append("G")
            
            prob.linear_constraints.add(lin_expr = G, senses = senses, rhs = h)
            prob.solve()
            x = prob.solution.get_values()
            print(x)        

        for i in range(self._n_var):
            self._card.append(x[i])
        
        # # !!!!!!!!!!!!!!!! Just for drawing figure !!!!!!!!!!!!!!!!!!!!
        # print("!!!!!!! Draw figure !!!!!!! [Please delete this part]")
        # with open("hdcs_spl%f_b%d_tr%d.txt" % (split_threshold, buckets_limit, len(self.train_list)), "w") as fout:
        #     for i in range(len(self._hcs)):
        #         for j in range(self.dim - 1):
        #             fout.write(str(self._hcs[i].bl[j]) + ",")
        #         fout.write(str(self._hcs[i].bl[self.dim - 1]) + ",")
        #         for j in range(self.dim - 1):
        #             fout.write(str(self._hcs[i].tr[j]) + ",")
        #         fout.write(str(self._hcs[i].tr[self.dim - 1]) + ",")
        #         fout.write(str(self._card[i]) + "\n")
        # # !!!!!!!!!!!!!!!! Just for drawing figure !!!!!!!!!!!!!!!!!!!!
            
        time_3 = time.time()
        rms_error = 0.0
        linf_error = 0.0
        for i in range(self.n):
            sel = self.train_list[i][1]
            est_sel = 0.0
            for j in range(self._n_var):
                area = self._hcs[j].area
                d = self._card[j]
                int_area = self.train_list[i][0].intersectionAreaWithHypercube(self._hcs[j])
                est_sel += d / area * int_area
            est_sel = min(1.000, max(est_sel, 0.000))
            rms_error += (sel - est_sel) ** 2
            linf_error = max(linf_error, abs(sel - est_sel))
        rms_error = (rms_error / self.n) ** 0.5
        print("Training RMS Error : %.6f" % (rms_error))
        print("Training LInf Error : %.6f" % (linf_error))
        return time_3 - start_time, self._n_var
    def get_model(self):
        model = []
        for i in range(self._n_var):
            model.append(self._hcs[i].bl + self._hcs[i].tr + [self._card[i]])
        return model

    def evaluate(self, test_list, pointers):
        start_time = time.time()
        error = 0.0
        linf_error = 0.0
        test_len = len(test_list)
        est_result = []
        abs_error = []

        for i in range(test_len):
            sel = test_list[i][1]
            est_sel = 0.0
            for j in range(self._n_var):
                area = self._hcs[j].area
                d = self._card[j]
                int_area = test_list[i][0].intersectionAreaWithHypercube(self._hcs[j])
                est_sel += d / area * int_area

            # if est_sel >= 1.0 or est_sel <= 0.0:
            #     bad_test_count += 1
            #     est_sel = max(0.0 + epsilon, min(1.0 - epsilon, est_sel))
            est_sel = min(1.000, max(est_sel, 0.000))
            abs_error.append(abs(sel - est_sel))
            # print(sel, est_sel, abs(sel - est_sel))
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
