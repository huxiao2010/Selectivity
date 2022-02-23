import matplotlib.pyplot as plt
import numpy as np
x =[50, 200, 500, 1000, 2000]
xx =[50, 200]

QuickSel = [0.109, 0.15, 1.077, 5.917, 41.157]
GOHist = [0.015, 0.255, 0.883, 1.935, 4.372]
PtsHist  = [0.007, 0.123, 1.213, 15.294, 90.539]
Isomer = [0.328, 35.061]

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
plt.ylim(top = 2000)
plt.title("Orthogonal - Random Workload - Forest", fontsize = 14)
plt.legend(loc = 'upper right', ncol=2, fontsize =14)
plt.savefig('Training-Forest-Random.pdf')
plt.show()
