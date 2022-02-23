import matplotlib.pyplot as plt
import numpy as np
x =[50, 200, 500, 1000, 2000]
xx =[50, 200]

QuickSel = [0.021, 0.013, 0.01, 0.006, 0.004]
GOHist = [0.022, 0.018, 0.012, 0.011, 0.006]
PtsHist  = [0.031, 0.011, 0.006, 0.004, 0.003]
Isomer  = [0.017, 0.007]

plt.plot(x, QuickSel,'yv-', markersize = 8, label = 'QuickSel')
#plt.plot(xx, GAHist, 'mo-', markersize = 8, label = 'GAHist')
plt.plot(x, GOHist, 'bo-', markersize = 8, label = 'QuadHist')
plt.plot(x, PtsHist, 'm*-', markersize = 8, label = 'PtsHist')
plt.plot(xx, Isomer, 'ks-', markersize = 8, label = 'Isomer')
plt.xlabel('Number of training queries', fontsize = 14)
plt.ylabel('RMS error', fontsize = 14)
plt.xticks(x, fontsize = 14)
plt.yticks(fontsize = 14)
plt.title("Orthogonal - Data-Driven Workload - DMV", fontsize = 14)
plt.legend(loc = 'upper right', fontsize =14)
plt.savefig('RMS-DMV-Data.pdf')
plt.show()




