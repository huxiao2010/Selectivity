import matplotlib.pyplot as plt
import numpy as np
x =[50, 200, 500, 1000, 2000]
xx =[50, 200]
QuickSel = [0.106, 0.132, 1.054, 5.835, 40.485]
GAHist 	 = [0.11, 17.46] 
GOHist = [0.012, 0.181, 1.307, 6.462, 23.979]
PtsHist  = [0.006, 0.068,  0.584, 3.971, 23.528]
Isomer = [0.346, 86.892]

plt.plot(x, QuickSel,'cs-', markersize = 8, label = 'QuickSel')
plt.plot(xx, GAHist, 'mo-', markersize = 8, label = 'GAHist')
plt.plot(x, GOHist, 'yv-', markersize = 8, label = 'GOHist')
plt.plot(x, PtsHist, 'k*-', markersize = 8, label = 'PtsHist')
plt.plot(xx, Isomer, 'b.-', markersize = 8, label = 'Isomer')


plt.xlabel('Number of training queries', fontsize = 14)
plt.ylabel('Time (s)', fontsize = 14)
plt.yscale('log')
plt.xticks(x, fontsize = 14)
plt.yticks(fontsize = 14)
plt.title("Rectangle - Random Workload - Power")
plt.legend(loc = 'lower right')
plt.savefig('Training-Power-Random.pdf')
plt.show()
