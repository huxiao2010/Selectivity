import matplotlib.pyplot as plt
import numpy as np
x =[50, 200, 500, 1000, 2000]
xx =[50, 200]

QuickSel = [0.031, 0.161, 1.062, 5.818, 40.399]
GOHist = [0.015, 0.228, 1.694, 9.124, 45.105]
PtsHist  = [0.007, 0.131, 1.139, 7.144, 37.732]
Isomer = [169.245, 4448.806]

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
plt.title("Orthogonal - Data-Driven Workload - DMV", fontsize = 14)
plt.legend(loc = 'upper right', ncol=2, fontsize =14)
plt.savefig('Training-DMV-Data.pdf')
plt.show()
