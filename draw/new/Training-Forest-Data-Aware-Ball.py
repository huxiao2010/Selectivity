import matplotlib.pyplot as plt

x = [50, 200, 500, 1000, 2000]

PtsHist2 = [0.011, 0.181, 1.543, 9.749, 65.139]
PtsHist4 = [0.016, 0.217, 1.496, 7.068, 34.786]
PtsHist6 = [0.024, 0.302, 1.744, 7.475, 32.867]
PtsHist8 = [0.062, 0.497, 2.368, 8.728, 34.319]
PtsHist10 = [0.318, 1.68, 5.503, 15.757, 49.912]
QuadHist2  = [0.21, 3.783, 10.477, 21.469, 43.48]

plt.plot(x, QuadHist2, 'bo-', markersize = 8, label = 'QuadHist (d=2)')
plt.plot(x, PtsHist2,  color = 'k', marker = '*', markersize = 8, label = 'PtsHist (d=2)')
plt.plot(x, PtsHist4,  color = 'indigo', marker = 'P', markersize = 8, label = 'PtsHist (d=4)')
plt.plot(x, PtsHist6,  color = 'blueviolet', marker = 'X', markersize = 8, label = 'PtsHist (d=6)')
plt.plot(x, PtsHist8,  color = 'mediumorchid', marker = 'D', markersize = 8, label = 'PtsHist (d=8)')
plt.plot(x, PtsHist10, color = 'plum', marker = 's', markersize = 8, label = 'PtsHist (d=10)')

plt.xlabel('Number of training queries', fontsize = 14)
plt.ylabel('Time (s)', fontsize = 14)
plt.yscale('log')
plt.xticks(x, fontsize = 14)
plt.yticks(fontsize = 14)
plt.title("Ball - Data-Driven Workload - Forest", fontsize = 14)
plt.legend(loc = 'lower right', fontsize =14)
plt.savefig('Training-Forest-Data-Aware-Ball.pdf')
plt.show()
