import time
from random import randint
from matplotlib import pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline, interp1d
from bnb import BnB

def generate_adjacency_matrix(rank):
    matrix = [[0] * rank for i in range(rank)]

    for i in range(rank):
        for j in range(i + 1, rank):
            matrix[i][j] = matrix[j][i] = randint(1, 100)

    return matrix

def run_time_tests():
    rank = 50
    elapsed_time = []

    # for i in range(30):
    matrix = generate_adjacency_matrix(rank)
    algo = BnB(matrix)
    algo.start()
    start = time.time()
    while algo.is_alive():
        print("Current best tour:", algo.final_path, "- Current best cost:", algo.final_res)
        time.sleep(3)
    algo.join(timeout=60)
    end = time.time()
    elapsed_time.append((0, (end-start) * 1000))
        # print(i)

    return elapsed_time

res = run_time_tests()
# data = np.array(res)
#
# x, y = data.T
# x = np.array(x)
# y = np.array(y)
# X_Y_Spline = interp1d(x, y, kind = "cubic")
# X_ = np.linspace(x.min(), x.max(), 500)
# Y_ = X_Y_Spline(X_)
# plt.plot(X_, Y_)
# plt.show()