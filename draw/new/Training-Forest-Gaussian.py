import matplotlib.pyplot as plt
import numpy as np
x =[50, 200, 500, 1000, 2000]
xx =[50, 200]

QuickSel = [0.029, 0.162, 1.056, 5.809, 40.312]
GOHist = [0.015, 0.287, 1.783, 3.789, 9.486]
PtsHist  = [0.007, 0.128, 1.265, 10.92, 88.364]
Isomer = [1.598, 294.8]

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
plt.ylim(top = 8000)
plt.title("Orthogonal - Gaussian Workload - Forest", fontsize = 14)
plt.legend(loc = 'upper right', ncol=2, fontsize =14)
plt.savefig('Training-Forest-Gaussian.pdf')
plt.show()
