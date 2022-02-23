import pandas as pd
import matplotlib.pyplot as plot


#Training Time 
#
GOHist2   = [4.808, 57.153, 65.404, 19.27, 42.626]
QuickSel2 = [44.929, 54.507, 97.629,47.327, 47.678]
PtsHist2  = [64.809, 39.135, 35.875, 24.952, 10.598]
#
#GOHist1   = [2.177, 17.694, 16.676, 5.855, 9.354]
#QuickSel1 = [6.581, 6.859, 7.175, 7.813, 7.696]
#PtsHist1  = [10.439, 6.703, 6.219, 9.752, 1.612]

#color_list = ['c', 'm', 'y']
#index = ['2', '4', '6', '8', '10']
#df = pd.DataFrame({
#	'QuickSel': QuickSel2, 
#	'GOHist': GOHist2, 
#	'PtsHist': PtsHist2
#	}, index=index)
#ax = df.plot.bar(logy = True, width = 0.5, rot=0, color = color_list)

x = ['2', '4', '6', '8', '10']
plt.plot(x, QuickSel2,'yv', markersize = 12, label = 'QuickSel')
#plt.plot(xx, GAHist, 'mo-', markersize = 8, label = 'GAHist')
plt.plot(x, GOHist2, 'bo', markersize = 12, label = 'QuadHist')
plt.plot(x, PtsHist2, 'm*', markersize = 12, label = 'PtsHist')

plot.title("Rectangle - Data-Aware Workload - Forest", fontsize= 14)
plot.xlabel("Number of dimensions", fontsize= 14)
plot.yscale('log')
plot.ylabel("Time (s)", fontsize= 14)
plot.legend(loc = 'upper right', fontsize= 14)
plot.xticks(fontsize= 14)
plot.yticks(fontsize= 14)
plot.ylim([1,500])
plot.savefig('Dimension-Training-Forest-Data.pdf')
plot.show(block=True)




