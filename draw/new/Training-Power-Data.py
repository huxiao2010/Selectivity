import matplotlib.pyplot as plt
import numpy as np
x =[50, 200, 500, 1000, 2000]
xx =[50, 200]
QuickSel = [0.107, 0.143, 1.043, 5.792, 40.328]
#GAHist 	 = [0.103, 18.27] 
GOHist = [0.014, 0.201, 1.33, 3.851, 8.848]
PtsHist  = [0.004, 0.08, 0.639, 3.98, 24.462]
Isomer = [5.058, 837.265]
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
plt.title("Orthogonal - Data-Driven Workload - Power", fontsize = 14)
plt.legend(loc = 'upper right', ncol=2, fontsize =14)
plt.savefig('Training-Power-Data.pdf')
plt.show()
