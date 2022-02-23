import matplotlib.pyplot as plt
import numpy as np
x =[50, 200, 500, 1000, 2000]
xx =[50, 200]

QuickSel = [0.029, 0.168, 1.072, 5.823, 40.347]
GOHist = [0.016, 0.342, 1.091, 2.325, 5.05]
PtsHist  = [0.008, 0.131, 1.251, 10.364, 94.996]
Isomer = [1.829, 397.783]

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
plt.title("Orthogonal - Data-Driven Workload - Forest", fontsize = 14)
plt.legend(loc = 'upper right', ncol=2, fontsize =14)
plt.savefig('Training-Forest-Data.pdf')
plt.show()
