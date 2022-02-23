import matplotlib.patches as mpatches
import pandas as pd
import matplotlib.pyplot as plot
import matplotlib
matplotlib.rcParams['legend.handlelength'] = 1
matplotlib.rcParams['legend.handleheight'] = 1

QuickSel = [200, 800, 2000, 4000, 8000]
GOHist   = [199, 799, 1429, 1429, 1597]
PtsHist  = [197, 796, 1988, 3995, 7963]
Isomer  = [2255, 27855, 0, 0, 0]

index = ['50', '200', '500', '1000', '2000']
df = pd.DataFrame({
	'QuickSel': QuickSel, 
	#'GAHist': GAHist, 
	'QuadHist': GOHist,
	'PtsHist': PtsHist,
	'Isomer':Isomer
	}, index=index)
color_list = ['y', 'b', 'm', 'k']
ax = df.plot.bar(logy = True, width = 0.8, rot=0, color = color_list)


QuickSelLegend = mpatches.Patch(color='c', label='QuickSel')
#GAHistDataLegend = mpatches.Patch(color='m', label='GAHist')
GOHistLegend = mpatches.Patch(color='y', label='QuadHist')
PstHistLegend = mpatches.Patch(color='k', label='PtsHist')
IsomerLegend = mpatches.Patch(color ='b', label='Isomer')
#plot.legend(handles=[QuickSelLegend, GAHistDataLegend, GOHistLegend, PstHistLegend, IsomerLegend], loc = 'upper right', fontsize = 14, ncol = 2)

plot.ylim(top = 110000)
plot.legend(loc = 'upper right', fontsize = 14, ncol = 2)
plot.title("Orthogonal - Gaussian Workload - Forest", fontsize = 14)
plot.xlabel("Number of training queries", fontsize = 14)
plot.ylabel("Number of buckets", fontsize = 14)
plot.xticks(fontsize = 14)
plot.yticks(fontsize = 14)
ax.figure.savefig('Vars-Forest-Gaussian.pdf')
plot.show(block=True)