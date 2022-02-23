import matplotlib.pyplot as plt
x1 = [50, 200, 500, 1100]
y = [0.02, 0.04, 0.06]
x2 = [50, 200, 500]
QuickSel = [0.062, 0.021, 0.015, 0.009]
GAHist 	 = [0.026, 0.009, 0.004]
GOHist0  = [0.018, 0.012, 0.009, 0.008]  
GOHist00 = [0.021, 0.009, 0.004, 0.004]
GOHist000= [0.023, 0.008, 0.003, 0.002]

plt.plot(x1, QuickSel, 's', linestyle='-', label = "QuickSel", markersize =12, fillstyle='none', mew = 2, linewidth = 2) 
plt.plot(x2, GAHist, 'ko', linestyle='-', label = "GAHist", markersize = 12, fillstyle='none', mew = 2, linewidth = 2) 
plt.plot(x1, GOHist0, 'v', linestyle='-', label = "GOHist (0.01)", markersize = 12, fillstyle='none', mew = 2, linewidth = 2)
plt.plot(x1, GOHist00, '*', linestyle='-', label = "GOHist (0.001)", markersize = 12, fillstyle='none',  mew = 2,  linewidth = 2)
plt.plot(x1, GOHist000, 'yx', linestyle='-', label = "GOHist (0.0001)", markersize = 12, fillstyle='none',  mew = 2, linewidth = 2)
plt.xlabel('Number of training queries', fontsize = 20)
plt.ylabel('RMS error', fontsize = 20)
plt.xticks(x1, x1, fontsize = 20)
plt.yticks(y, y, fontsize = 20)
plt.legend(fontsize = 'large')
plt.savefig('RMS-Power-Random.pdf')
plt.clf()



import matplotlib.pyplot as plt
x1 = [50, 200, 500, 1100]
x2 = [50, 200, 500]
QuickSel = [0.033, 0.158, 1.054, 5.889]
GAHist 	 = [0.19, 17.396, 444.99]
GOHist0  = [0.023, 0.159, 0.502, 1.109]  
GOHist00 = [0.134, 1.45, 6.355, 15.266]
GOHist000= [1.837, 16.688, 109.582, 290.223]

plt.plot(x1, QuickSel, 's', linestyle='-', label = "QuickSel", markersize =12, fillstyle='none', mew = 2, linewidth = 2) 
plt.plot(x2, GAHist, 'ko', linestyle='-', label = "GAHist", markersize = 12, fillstyle='none', mew = 2, linewidth = 2) 
plt.plot(x1, GOHist0, 'v', linestyle='-', label = "GOHist (0.01)", markersize = 12, fillstyle='none', mew = 2, linewidth = 2)
plt.plot(x1, GOHist00, '*', linestyle='-', label = "GOHist (0.001)", markersize = 12, fillstyle='none',  mew = 2,  linewidth = 2)
plt.plot(x1, GOHist000, 'yx', linestyle='-', label = "GOHist (0.0001)", markersize = 12, fillstyle='none',  mew = 2, linewidth = 2)
plt.xlabel('Number of training queries', fontsize = 20)
plt.ylabel('Time (s)', fontsize = 20)
plt.yscale('log')
plt.xticks(x1, x1, fontsize = 20)
plt.yticks(y, y, fontsize = 20)
plt.legend(fontsize = 'large')
plt.savefig('Training-Power-Random.pdf')
plt.close()

import matplotlib.pyplot as plt
x1 = [50, 200, 500, 1100]
x2 = [50, 200, 500]
#QuickSel = [0,0,0,0]
GAHist 	 = [2500, 40000, 250000]
GOHist0  = [271, 652, 652, 691]  
GOHist00 = [1795, 4252, 5107, 5629]
GOHist000= [22274, 43078, 45835, 48298]

plt.plot(x1, QuickSel, 's', linestyle='-', label = "QuickSel", markersize =12, fillstyle='none', mew = 2, linewidth = 2) 
plt.plot(x2, GAHist, 'ko', linestyle='-', label = "GAHist", markersize = 12, fillstyle='none', mew = 2, linewidth = 2) 
plt.plot(x1, GOHist0, 'v', linestyle='-', label = "GOHist (0.01)", markersize = 12, fillstyle='none', mew = 2, linewidth = 2)
plt.plot(x1, GOHist00, '*', linestyle='-', label = "GOHist (0.001)", markersize = 12, fillstyle='none',  mew = 2,  linewidth = 2)
plt.plot(x1, GOHist000, 'yx', linestyle='-', label = "GOHist (0.0001)", markersize = 12, fillstyle='none',  mew = 2, linewidth = 2)
plt.xlabel('Number of training queries', fontsize = 20)
plt.ylabel('Time (s)', fontsize = 20)
plt.yscale('log')
plt.xticks(x1, x1, fontsize = 20)
plt.yticks(y, y, fontsize = 20)
plt.legend(fontsize = 'large')
plt.savefig('Bucket-Power-Random.pdf')
plt.close()