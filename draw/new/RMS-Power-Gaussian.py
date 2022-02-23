import matplotlib.pyplot as plt
x =[50, 200, 500, 1000, 2000]
xx =[50, 200]
xxx = [50, 200, 500, 1000]
QuickSel = [0.076, 0.022, 0.012, 0.01, 0.005]
#GAHist 	 = [0.069, 0.007] 
GOHist = [0.063, 0.012, 0.012, 0.01, 0.01]
PtsHist  = [0.068, 0.016, 0.012, 0.015, 0.008]
Isomer = [0.045, 0.007]


plt.plot(x, QuickSel,'yv-', markersize = 8, label = 'QuickSel')
#plt.plot(xx, GAHist, 'mo-', markersize = 8, label = 'GAHist')
plt.plot(x, GOHist, 'bo-', markersize = 8, label = 'GOHist')
plt.plot(x, PtsHist, 'm*-', markersize = 8, label = 'PtsHist')
plt.plot(xx, Isomer,'ks-', markersize = 8, label = 'Isomer')

plt.xlabel('Number of training queries', fontsize = 14)
plt.ylabel('RMS error', fontsize = 14)
plt.xticks(x, fontsize = 14)
plt.yticks(fontsize = 14)
plt.title("Orthogonal - Gaussian Workload - Power", fontsize =14)
plt.legend(loc = 'upper right', fontsize= 14)
plt.savefig('RMS-Power-Gaussian.pdf')
plt.show()
