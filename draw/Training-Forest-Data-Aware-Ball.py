import matplotlib.pyplot as plt

x = [50, 200, 500, 1000, 2000]
xx = [50, 200]

PtsHist2 = [0.012, 0.191, 1.769, 10.787, 71.382]
PtsHist4 = [0.023, 0.304, 1.963, 9.194, 44.895]
PtsHist6 = [0.036, 0.426, 2.354, 9.618, 41.354]
PtsHist8 = [0.090, 0.694, 3.112, 11.112, 41.799]
PtsHist10 = [0.507, 2.365, 7.209, 19.458, 59.778]
GOHist  = [0.039, 0.152, 0.415, 0.886, 1.794]
#GAHist = [9.846, 596.414]

#plt.plot(xx, GAHist, 'co-', markersize = 8, label = 'GAHist (d=2)')
plt.plot(x, GOHist, 'bo-', markersize = 8, label = 'QuadHist (d=2)')
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
plt.title("Ball - Data-aware Workload - Forest", fontsize = 14)
plt.legend(loc = 'lower right', fontsize =14)
plt.savefig('Training-Forest-Data-Aware-Ball.pdf')
plt.show()
