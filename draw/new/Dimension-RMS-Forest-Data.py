import matplotlib.pyplot as plt

GOHist2    = [0.004517, 0.007306, 0.012465, 0.029838, 0.050209]
QuickSel2  = [0.00148, 0.006, 0.01297, 0.03, 0.034]
PtsHist2   = [0.00213, 0.00589, 0.00722, 0.02252, 0.04828]

x = ['2', '4', '6', '8', '10']

plt.plot([2, 4, 6, 8, 10], GOHist2, 'bo', markersize = 12, label = 'QuadHist')
plt.plot([2, 4, 6, 8, 10], QuickSel2,'yv', markersize = 12, label = 'QuickSel')
plt.plot([2, 4, 6, 8, 10], PtsHist2, 'm*', markersize = 12, label = 'PtsHist')

plt.legend(loc = 'upper left', fontsize= 14, ncol = 2)
plt.title("Orthogonal - Data-Driven Workload - Forest", fontsize= 14)
plt.xlabel("Number of dimensions", fontsize= 14)
plt.ylabel("RMS error", fontsize= 14)
plt.xticks([2, 4, 6, 8, 10], x, fontsize= 14)
plt.yticks(fontsize= 14)
#plt.ylim([0, 0.04])
plt.savefig('Dimension-RMS-Forest-Data-1000.pdf')
plt.show()



