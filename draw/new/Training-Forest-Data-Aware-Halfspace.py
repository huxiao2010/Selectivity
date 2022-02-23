import matplotlib.pyplot as plt

x = [50, 200, 500, 1000, 2000]

PtsHist2 = [0.009, 0.145, 1.519, 11.568, 75.631]
PtsHist4 = [0.011, 0.16, 1.2, 6.707, 38.446]
PtsHist6 = [0.013, 0.183, 1.256, 5.753, 27.896]
PtsHist8 = [0.016, 0.207, 1.274, 5.444, 23.452]
PtsHist10 = [0.016, 0.247, 1.436, 5.914, 24.259]
QuadHist2  = [0.936, 14.798, 52.764, 104.81, 210.359]

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
plt.title("Halfspace - Data-Driven Workload - Forest", fontsize = 14)
plt.legend(loc = 'lower right', fontsize =14)
plt.savefig('Training-Forest-Data-Aware-Halfspaces.pdf')
plt.show()
