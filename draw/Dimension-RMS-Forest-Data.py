import pandas as pd
import matplotlib.pyplot as plt

GOHist2    = [0.001, 0.005, 0.009, 0.031, 0.025]
QuickSel2  = [0.00136, 0.0067, 0.009, 0.026, 0.023]
PtsHist2   = [0.001, 0.005, 0.006, 0.015, 0.019]


#color_list = ['b', 'y', 'm']
#index = ['2', '4', '6', '8', '10']
#df = pd.DataFrame({
#	'QuickSel': QuickSel2, 
#	'QuadHist': GOHist2, 
#	'PtsHist': PtsHist2
#	}, index=index)
#ax = df.plot.bar(width = 0.5, rot=0, color = color_list)

x = ['2', '4', '6', '8', '10']
plt.plot(x, QuickSel2,'yv', markersize = 12, label = 'QuickSel')
#plt.plot(xx, GAHist, 'mo-', markersize = 8, label = 'GAHist')
plt.plot(x, GOHist2, 'bo', markersize = 12, label = 'QuadHist')
plt.plot(x, PtsHist2, 'm*', markersize = 12, label = 'PtsHist')

plt.legend(loc = 'upper left', fontsize= 14)
plt.title("Rectangle - Data-Aware Workload - Forest", fontsize= 14)
plt.xlabel("Number of dimensions", fontsize= 14)
plt.ylabel("RMS error", fontsize= 14)
plt.xticks(fontsize= 14)
plt.yticks(fontsize= 14)
plt.ylim([0, 0.04])
plt.savefig('Dimension-RMS-Forest-Data.pdf')
plt.show()



