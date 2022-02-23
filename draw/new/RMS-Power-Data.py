import matplotlib.pyplot as plt
import numpy as np
x =[50, 200, 500, 1000, 2000]
xx =[50, 200]
QuickSel = [0.056, 0.026, 0.014, 0.006, 0.004]
#GAHist 	 = [0.042, 0.011] 
GOHist = [0.077, 0.023, 0.012, 0.004, 0.003]
PtsHist  = [0.065, 0.032,  0.014, 0.008, 0.003]
Isomer  = [0.043, 0.007]
plt.plot(x, QuickSel,'yv-', markersize = 8, label = 'QuickSel')
#plt.plot(xx, GAHist, 'mo-', markersize = 8, label = 'GAHist')
plt.plot(x, GOHist, 'bo-', markersize = 8, label = 'QuadHist')
plt.plot(x, PtsHist, 'm*-', markersize = 8, label = 'PtsHist')
plt.plot(xx, Isomer, 'ks-', markersize = 8, label = 'Isomer')
plt.xlabel('Number of training queries', fontsize = 14)
plt.ylabel('RMS error', fontsize = 14)
plt.xticks(x, fontsize = 14)
plt.yticks(fontsize = 14)
plt.title("Orthogonal - Data-Driven Workload - Power", fontsize = 14)
plt.legend(loc = 'upper right', fontsize =14)
plt.savefig('RMS-Power-Data.pdf')
plt.show()





