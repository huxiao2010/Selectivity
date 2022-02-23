import matplotlib.pyplot as plt

x = [50, 200, 500, 1000, 2000]
xx = [50, 200]

PtsHist2 = [0.049, 0.014, 0.006, 0.004, 0.002]
PtsHist4 = [0.074, 0.036, 0.023, 0.015, 0.011]
PtsHist6 = [0.1, 0.059, 0.039, 0.03, 0.021]
PtsHist8 = [0.233, 0.124, 0.086, 0.071, 0.05]
PtsHist10= [0.208, 0.131, 0.11, 0.088, 0.073]
GOHist  = [0.028, 0.005, 0.001, 0.001, 0.001]
#GAHist = [0.066, 0.016]


#plt.plot(xx, GAHist, 'co-', markersize = 8, label = 'GAHist (d=2)')
plt.plot(x, GOHist, 'bo-', markersize = 8, label = 'QuadHist (d=2)')
plt.plot(x, PtsHist2,  color = 'k', marker = '*', markersize = 8, label = 'PtsHist (d=2)')
plt.plot(x, PtsHist4,  color = 'indigo', marker = 'P', markersize = 8, label = 'PtsHist (d=4)')
plt.plot(x, PtsHist6,  color = 'blueviolet', marker = 'X', markersize = 8, label = 'PtsHist (d=6)')
plt.plot(x, PtsHist8,  color = 'mediumorchid', marker = 'D', markersize = 8, label = 'PtsHist (d=8)')
plt.plot(x, PtsHist10, color = 'plum', marker = 's', markersize = 8, label = 'PtsHist (d=10)')


plt.xlabel('Number of training queries', fontsize = 14)
plt.ylabel('RMS error', fontsize = 14)
plt.xticks(x, fontsize = 14)
plt.yticks(fontsize = 14)
plt.title("Ball - Data-Aware Workload - Forest", fontsize =14)
plt.legend(loc = 'upper right', fontsize= 14)
plt.savefig('RMS-Forest-Data-Aware-Ball.pdf')
plt.show()
