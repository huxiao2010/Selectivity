import matplotlib.pyplot as plt

x = [50, 200, 500, 1000, 2000]
xx = [50, 200, 500]
xxx = [50, 200, 500, 1000]

PtsHist2 = [0.066, 0.017, 0.006, 0.003, 0.002]
PtsHist4 = [0.075, 0.033, 0.015, 0.01, 0.007]
PtsHist6 = [0.083, 0.046, 0.028, 0.021, 0.014]
PtsHist8 = [0.164, 0.083, 0.066, 0.044, 0.035]
PtsHist10= [0.2, 0.106, 0.088, 0.08, 0.044]
GOHist  = [0.032, 0.005, 0.001, 0.001, 0.001]
#GAHist = [0.048, 0.018, 0.007, 0.003]

#plt.plot(xxx, GAHist, 'co-', markersize = 8, label = 'GAHist (d=2)')
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
plt.title("Halfspace - Data-Aware Workload - Forest", fontsize =14)
plt.legend(loc = 'upper right', fontsize= 14)
plt.savefig('RMS-Forest-Data-Aware-Halfspace.pdf')
plt.show()
