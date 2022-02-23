import matplotlib.pyplot as plt

x = [50, 200, 500, 1000, 2000]

PtsHist2 = [0.04273, 0.01455, 0.0064, 0.00438, 0.00217]
PtsHist4 = [0.06677, 0.04269, 0.02437, 0.01812, 0.01141]
PtsHist6 = [0.10406, 0.05821, 0.04298, 0.0341, 0.02165]
PtsHist8 = [0.24969, 0.13353, 0.0929, 0.07098, 0.05368]
PtsHist10 = [0.22129, 0.13744, 0.11308, 0.08768, 0.07565]
QuadHist2  = [0.021125, 0.007908, 0.001748, 0.000397, 0.000382]

plt.plot(x, QuadHist2, 'bo-', markersize = 8, label = 'QuadHist (d=2)')
plt.plot(x, PtsHist2,  color = 'k', marker = '*', markersize = 8, label = 'PtsHist (d=2)')
plt.plot(x, PtsHist4,  color = 'indigo', marker = 'P', markersize = 8, label = 'PtsHist (d=4)')
plt.plot(x, PtsHist6,  color = 'blueviolet', marker = 'X', markersize = 8, label = 'PtsHist (d=6)')
plt.plot(x, PtsHist8,  color = 'mediumorchid', marker = 'D', markersize = 8, label = 'PtsHist (d=8)')
plt.plot(x, PtsHist10, color = 'plum', marker = 's', markersize = 8, label = 'PtsHist (d=10)')

plt.xlabel('Number of training queries', fontsize = 14)
plt.ylabel('RMS error', fontsize = 14)
plt.xticks(x, fontsize = 14)
plt.yticks(fontsize = 14)
plt.title("Ball - Data-Driven Workload - Forest", fontsize =14)
plt.legend(loc = 'upper right', fontsize= 14)
plt.savefig('RMS-Forest-Data-Aware-Ball.pdf')
plt.show()
