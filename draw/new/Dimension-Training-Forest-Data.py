import matplotlib.pyplot as plt

GOHist2   = [11.07, 9.603, 9.027, 8.992, 7.491]
QuickSel2 = [7.189, 6.859, 7.175, 7.813, 7.696]
PtsHist2  = [10.364, 8.873, 6.535, 5.236, 5.219]

x = ['2', '4', '6', '8', '10']
y = ['6', '7', '8', '9', '10']

plt.plot([2, 4, 6, 8, 10], QuickSel2,'yv', markersize = 12, label = 'QuickSel')
plt.plot([2, 4, 6, 8, 10], GOHist2, 'bo', markersize = 12, label = 'QuadHist')
plt.plot([2, 4, 6, 8, 10], PtsHist2, 'm*', markersize = 12, label = 'PtsHist')

plt.title("Orthogonal- Data-Driven Workload - Forest", fontsize= 14)
plt.xlabel("Number of dimensions", fontsize= 14)
# plt.yscale('log')
plt.ylabel("Time (s)", fontsize= 14)
plt.legend(loc = 'upper right', fontsize= 14)
plt.xticks([2, 4, 6, 8, 10], x, fontsize= 14)
plt.yticks(fontsize= 14)
# plt.ylim([1,500])
plt.savefig('Dimension-Training-Forest-Data-1000.pdf')
plt.show(block=True)




