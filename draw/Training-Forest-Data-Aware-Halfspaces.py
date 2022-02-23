import matplotlib.pyplot as plt

x = [50, 200, 500, 1000, 2000]
xx = [50, 200, 500]

PtsHist2 = [0.01, 0.17, 1.639, 13.985, 103.454]
PtsHist4 = [0.011, 0.191, 1.428, 8.152, 45.417]
PtsHist6 = [0.015, 0.184, 1.361, 6.436, 31.785]
PtsHist8 = [0.019, 0.215, 1.432, 5.954, 25.55]
PtsHist10 = [0.016, 0.263, 1.666, 6.638, 28.194]
GOHist  = [1.967, 7.82, 19.607, 39.027, 79.19]
#GAHist = [4.463, 185.991, 1548.729]

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
plt.title("Halfspaces - Data-aware Workload - Forest", fontsize = 14)
plt.legend(loc = 'lower right', fontsize =14)
plt.savefig('Training-Forest-Data-Aware-Halfspaces.pdf')
plt.show()
