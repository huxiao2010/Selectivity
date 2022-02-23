import matplotlib.pyplot as plt
import numpy as np
x = [50, 200, 500, 1000, 2000]
xx = [50, 200]
QuickSel = [0.033, 0.147, 1.044, 5.839, 43.293]
#GAHist 	 = [0.103, 18.27] 
GOHist = [0.014, 0.23, 1.65, 8.372, 24.045]
PtsHist  = [0.006, 0.098, 0.682, 2.726, 17.084]
Isomer = [1.976, 577.604]
plt.plot(x, QuickSel,'yv-', markersize = 8, label = 'QuickSel')
#plt.plot(xx, GAHist, 'mo-', markersize = 8, label = 'GAHist')
plt.plot(x, GOHist, 'bo-', markersize = 8, label = 'QuadHist')
plt.plot(x, PtsHist, 'm*-', markersize = 8, label = 'PtsHist')
plt.plot(xx, Isomer, 'ks-', markersize = 8, label = 'Isomer')
plt.xlabel('Number of training queries', fontsize = 14)
plt.ylabel('Time (s)', fontsize = 14)
plt.yscale('log')
plt.xticks(x, fontsize = 14)
plt.yticks(fontsize = 14)
plt.title("Orthogonal - Gaussian Workload - Power", fontsize = 14)
plt.legend(loc = 'upper right', ncol=2, fontsize =14)
plt.savefig('Training-Power-Gaussian.pdf')
plt.show()
