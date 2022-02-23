import pandas as pd
import matplotlib.pyplot as plot


GOHist2   = [1006, 5086, 6364, 2551, 7162]
QuickSel2 = [8000, 8000, 8000, 8000, 8000]
PtsHist2  = [6812, 5860, 6440, 5172, 3902]

#GOHist1  = [976, 3586, 3592, 2551, 3070]
#QuickSel1 = [4000, 4000, 4000, 4000, 4000]
#PtsHist1  = [3416, 2992, 3201, 2603, 1488]
color_list = ['b', 'y', 'm']
index = ['2', '4', '6', '8', '10']
df = pd.DataFrame({
	'QuickSel': QuickSel2, 
	'GOHist': GOHist2, 
	'PtsHist': PtsHist2,
	}, index=index)
ax = df.plot.bar(logy = True, width = 0.5, rot=0, color = color_list)
plot.title("Rectangle - Data-Aware Workload - Forest", fontsize= 14)
plot.xlabel("Number of dimensions", fontsize= 14)
plot.ylabel("Number of buckets", fontsize= 14)
plot.xticks(fontsize= 14)
plot.yticks(fontsize= 14)
plot.legend(ncol =3, fontsize= 14)
plot.ylim([1, 100000])
ax.figure.savefig('Dimension-Vars-Forest-Data.pdf')
plot.show(block=True)




