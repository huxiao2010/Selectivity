import matplotlib.pyplot as plt
x =[50, 200, 500, 1000, 2000]
xx =[50, 200]

QuickSel = [0.033, 0.147, 1.044, 5.839, 43.293]
GAHist 	 = [0.103, 13.864] 
GOHist = [0.014, 0.23, 1.65, 8.372, 24.045]
PtsHist  = [0.006, 0.098, 0.682, 2.726, 17.084]
Isomer = [1.976, 577.604]

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
plt.title("Rectangle - Gaussian Workload - Power")
plt.legend(loc = 'lower right')
plt.savefig('Training-Power-Gaussian.pdf')
plt.show()
