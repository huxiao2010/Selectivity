import matplotlib.pyplot as plt

x = [50, 200, 500, 1000, 2000]

PtsHist2 = [0.05905, 0.01492, 0.00555, 0.00263, 0.00173]
PtsHist4 = [0.07463, 0.03209, 0.01672, 0.00999, 0.00745]
PtsHist6 = [0.08279, 0.04571, 0.02815, 0.02149, 0.01442]
PtsHist8 = [0.16143, 0.08282, 0.06418, 0.04616, 0.04107]
PtsHist10 = [0.19966, 0.10556, 0.08932, 0.08026, 0.0464]
QuadHist2 = [0.015946, 0.011358, 0.001902, 0.000755, 0.000277]

plt.plot(x, QuadHist2, 'bo-', markersize = 8, label = 'QuadHist (d=2)')
plt.plot(x, PtsHist2,  color = 'k', marker = '*', markersize = 8, label = 'PtsHist (d=2)')
plt.plot(x, PtsHist4,  color = 'indigo', marker = 'P', markersize = 8, label = 'PtsHist (d=4)')
plt.plot(x, PtsHist6,  color = 'blueviolet', marker = 'X', markersize = 8, label = 'PtsHist (d=6)')
plt.plot(x, PtsHist8,  color = 'mediumorchid', marker = 'D', markersize = 8, label = 'PtsHist (d=8)')
plt.plot(x, PtsHist10, color = 'plum', marker = 's', markersize = 8, label = 'PtsHist (d=10)')

plt.xlabel('Number of training queries', fontsize = 14)
plt.ylabel('RMS error', fontsize = 14)
plt.xticks(x, fontsize = 14)
plt.yticks([0.00, 0.05, 0.10, 0.15, 0.20], fontsize = 14)
plt.title("Halfspace - Data-Driven Workload - Forest", fontsize =14)
plt.legend(loc = 'upper right', fontsize= 14)
plt.savefig('RMS-Forest-Data-Aware-Halfspace.pdf')
plt.show()
