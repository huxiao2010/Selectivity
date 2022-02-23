import matplotlib.pyplot as plt
import numpy as np
x =[50, 200, 500, 1000, 2000]
xx =[50, 200]

QuickSel = [0.126, 0.037, 0.025, 0.014, 0.012]
GOHist = [0.048, 0.016, 0.008, 0.007, 0.005]
PtsHist  = [0.029, 0.023, 0.011, 0.018, 0.007]
Isomer  = [0.031, 0.012]

plt.plot(x, QuickSel,'yv-', markersize = 8, label = 'QuickSel')
#plt.plot(xx, GAHist, 'mo-', markersize = 8, label = 'GAHist')
plt.plot(x, GOHist, 'bo-', markersize = 8, label = 'QuadHist')
plt.plot(x, PtsHist, 'm*-', markersize = 8, label = 'PtsHist')
plt.plot(xx, Isomer, 'ks-', markersize = 8, label = 'Isomer')
plt.xlabel('Number of training queries', fontsize = 14)
plt.ylabel('RMS error', fontsize = 14)
plt.xticks(x, fontsize = 14)
plt.yticks(fontsize = 14)
plt.title("Orthogonal - Data-Driven Workload - Census", fontsize = 14)
plt.legend(loc = 'upper right', fontsize =14)
plt.savefig('RMS-Census-Data.pdf')
plt.show()





