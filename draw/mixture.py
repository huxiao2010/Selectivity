import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors

# Create some mock data on Power
x = [0, 0.25, 0.5, 0.75, 1]
y = [0, 0.25, 0.5, 0.75, 1]
"""
# GOHIST Forest 2d 0.001
GOHist0 = [0.0013289, 0.0013261, 0.0013159, 0.0013911, 0.0014123]
GOHist025 = [0.0014197, 0.0013767, 0.0013243, 0.0013457, 0.0013361]
GOHist05= [0.0014006, 0.0013921, 0.0013621, 0.0013793, 0.0013482]
GOHist075 = [0.0014749, 0.0014429, 0.0013754, 0.0013827, 0.0012896]
GOHist1= [0.002809, 0.0025561, 0.0021247, 0.0017755, 0.001209]
"""

# PTSHIST Forest 2d 0.1 0.1



dz = PTSHist1 = [0.0054234
,0.0049383
,0.004331
,0.0036736
,0.0028321
,0.0022995
,0.0021803
,0.0021558
,0.002148
,0.0021037
,0.0018079
,0.0018788
,0.0019146
,0.0019431
,0.0019582
,0.0016952
,0.0017447
,0.0017941
,0.0017959
,0.0017989
,0.0014609
,0.0016008
,0.0016736
,0.0017706
,0.0018545]




colors = []
for i in range(len(dz)):
    color_z = 1.0
    if dz[i] > 0.0017:
        color_z /= 2
    if dz[i] > 0.0019:
        color_z /= 2
    if dz[i] > 0.003:
        color_z /= 2
    if dz[i] > 0.004:
        color_z /= 2
    colors.append([1.0, 1 - color_z, 1 - color_z])


for i in range(len(x)):
	for j in range(len(y)):
		plt.scatter(x[i], y[j], color = matplotlib.colors.to_hex(colors[i*5+j]))

plt.show()







A = [[0.0014609, 0.0016008, 0.0016736, 0.0017706, 0.0018545],
  [0.0016952, 0.0017447, 0.0017941, 0.0017959, 0.0017989],
  [0.0018079, 0.0018788, 0.0019146, 0.0019431, 0.0019582],
  [0.0022995, 0.0021803, 0.0021558, 0.002148, 0.0021037],
  [0.0054234, 0.0049383, 0.004331, 0.0036736, 0.0028321]]


"""
# GOHIST Power-2d 0.001
GOHist0 = [0.0035911
,0.0031922
,0.0026915
,0.002597
,0.0021547]
GOHist025 = [0.0038674
,0.0031514
,0.002314
,0.0021022
,0.0017369]
GOHist05= [0.0041338
,0.0033993
,0.0023345
,0.0019969
,0.0011783]
GOHist075 = [0.0036647
,0.0029264
,0.0021603
,0.0018029
,0.0010132]
GOHist1= [0.0024779
,0.0021277
,0.0016386
,0.0013545
,0.0008211]
# PTSHIST Power 2d 0.1 0.1
PTSHist0 = [0.0034551
,0.0029092
,0.0023339
,0.0019017
,0.0015698]
PTSHist025 = [0.0035491
,0.0030715
,0.0027248
,0.0023997
,0.0017201]
PTSHist05 = [0.0047892
,0.0041766
,0.0033125
,0.002999
,0.002036]
PTSHist075 = [0.0058016
,0.0051713
,0.0041035
,0.0034564
,0.0023568]
PTSHist1 = [0.0125749
,0.0112023
,0.0091448
,0.0063748
,0.003688]
"""

fig, ax1 = plt.subplots()

ax1.set_xlabel('Test workload: random / data-aware', size = 14)
ax1.set_xticks(x) 
ax1.plot(x, PTSHist0, 'cs-', markersize = 8, label = '0/1')
ax1.plot(x, PTSHist025, 'mo-', markersize = 8, label = '0.25/0.75')
ax1.plot(x, PTSHist05, 'yv-', markersize = 8, label = '0.5/0.5')
ax1.plot(x, PTSHist075,'b*-', markersize = 8, label = '0.75/0.25')
ax1.plot(x, PTSHist1, 'kP-', markersize = 8, label = '1/0')
#ax1.tick_params(axis='y')
#ax1.ylabel('RMS Error (training queries from Random workload')


#ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

#ax1.plot(x, QuickSelDR, 'cs', linestyle = ':', markersize = 8, label = 'QuickSel (Data-Aware)')
#ax1.plot(x, GOHistDR, 'mo', linestyle = ':', markersize = 8, label = 'GOHist (Data-Aware)')
#ax1.plot(x, PtsHistDR, 'yv', linestyle = ':', markersize = 8, label = 'PtsHist (Data-Aware)')
#ax1.ticklabel_format(axis='y', style = 'sci')
#ax1.ylabel('RMS Error')
#ax1.legend(loc = 'upper right')

#fig.tight_layout()  # otherwise the rigt y-label is slightly clipped


ax1.legend(loc='upper right', title = 'Training workload: \n random/data-aware')
plt.xticks(x, ['0/1', '0.25/0.75', '0.5/0.5', '0.75/0.25', '1/0'], fontsize = 14)
plt.yticks(fontsize = 14) 
plt.ylabel('RMS Error', fontsize = 14)
plt.title("Rectangle - Forest", fontsize = 14)
plt.savefig("mixture.pdf")
plt.show()
