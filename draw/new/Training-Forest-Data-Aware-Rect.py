import matplotlib.pyplot as plt

x = [50, 200, 500, 1000, 2000]

PtsHist2 = [0.008, 0.131, 1.251, 10.364, 94.996]
PtsHist4 = [0.009, 0.156, 1.336, 8.873, 52.946]
PtsHist6 = [0.01, 0.15, 1.141, 6.535, 38.529]
PtsHist8 = [0.011, 0.149, 1.041, 5.236, 27.822]
PtsHist10 = [0.011, 0.162, 1.395, 5.219, 25.625]

# QuadHist2  = [0.015, 0.225, 2.006, 11.07, 85.317]
# QuadHist4 = [0.022, 0.299, 1.743, 9.603, 49.284]
# QuadHist6 = [0.023, 0.36, 2.195, 9.027, 38.094]

plt.plot(x, PtsHist2,  color = 'k', marker = '*', markersize = 8, label = 'PtsHist (d=2)')
plt.plot(x, PtsHist4,  color = 'indigo', marker = 'P', markersize = 8, label = 'PtsHist (d=4)')
plt.plot(x, PtsHist6,  color = 'blueviolet', marker = 'X', markersize = 8, label = 'PtsHist (d=6)')
plt.plot(x, PtsHist8,  color = 'mediumorchid', marker = 'D', markersize = 8, label = 'PtsHist (d=8)')
plt.plot(x, PtsHist10, color = 'plum', marker = 's', markersize = 8, label = 'PtsHist (d=10)')

# plt.plot(x, QuadHist2, color = '#159f49', marker = '*', markersize = 8, label = 'QuadHist (d=2)')
# plt.plot(x, QuadHist4, color = '#5fedcf', marker = 'P', markersize = 8, label = 'QuadHist (d=4)')
# plt.plot(x, QuadHist6, color = '#fff308', marker = 'X', markersize = 8, label = 'QuadHist (d=6)')

plt.xlabel('Number of training queries', fontsize = 14)
plt.ylabel('Time (s)', fontsize = 14)
plt.yscale('log')
plt.xticks(x, fontsize = 14)
plt.yticks(fontsize = 14)
plt.title("Orthogonal - Data-Driven Workload - Forest", fontsize = 14)
plt.legend(loc = 'lower right', fontsize =14)
plt.savefig('Training-Forest-Data-Aware-Rect.pdf')
plt.show()
