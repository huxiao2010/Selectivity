import numpy as np
import matplotlib.pyplot as plt

# Create some mock data
x =[50, 200, 500, 1000, 2000]
errorGOHist0    = [0.093,  0.036, 0.036, 0.019, 0.018]
errorGOHist00   = [0.053, 0.016, 0.011, 0.008, 0.005]
errorGOHist000  = [0.033, 0.024, 0.011, 0.005, 0.004]
GOHist0	  = [49, 76, 79, 109, 121]
GOHist00  = [550, 943, 1177, 1348, 1606]  
GOHist000 = [5344, 9439, 10978, 14860, 17326] 

fig, ax1 = plt.subplots()

ax1.set_xlabel('Number of training queries', size  = 14)
ax1.set_xticks(x) 
# ax1.set_yticks([0, 0.03, 0.06, 0.09, 0.12, 0.15])
ax1.plot(x, errorGOHist0, 'cs-', markersize = 8, label = 'RMS Error (0.1)')
ax1.plot(x, errorGOHist00, 'mo-', markersize = 8, label = 'RMS Error (0.01)')
ax1.plot(x, errorGOHist000, 'yv-', markersize = 8, label = 'RMS Error (0.001)')
ax1.tick_params(axis='y', labelsize=14)
ax1.legend(loc = 'upper left', fontsize = 14)
ax1.set_ylim([0,0.16])
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

ax2.set_yscale('log')  # we already handled the x-label with ax1
ax2.plot(x, GOHist0,'cs', linestyle = ':', markersize = 8, label = '#Buckets (0.1)')
ax2.plot(x, GOHist00, 'mo', linestyle = ':', markersize = 8, label = '#Buckets (0.01)')
ax2.plot(x, GOHist000, 'yv', linestyle = ':', markersize = 8, label = '#Buckets (0.001)')
ax2.tick_params(axis='y', labelsize=14)
ax2.set_ylim([1,2000000])
ax2.legend(loc = 'upper right', fontsize =14)
plt.xticks(fontsize=14)

#fig.tight_layout()  # otherwise the rigt y-label is slightly clipped
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14) 
plt.title("Rectangle - Data-aware Workload of Power", fontsize = 14)
plt.tight_layout()
plt.savefig("GOHist-2.pdf")
plt.show


##########################################################################
import numpy as np
import matplotlib.pyplot as plt

# Create some mock data
x =[50, 200, 500, 1000, 2000]
errorGOHist0    = [0.093,  0.036, 0.036, 0.019, 0.018]
errorGOHist00   = [0.053, 0.016, 0.011, 0.008, 0.005]
errorGOHist000  = [0.033, 0.024, 0.011, 0.005, 0.004]



train50   = [0.093, 0.053, 0.033, ] 
train200  = [0.036, 0.016, 0.024, ]
train500  = [0.036, 0.011, 0.011, ]
train1000 = [0.019, 0.008, 0.005, ]
train2000 = [0.018, 0.005, 0.004, ]

GOHist0	  = [49, 76, 79, 109, 121]
GOHist00  = [550, 943, 1177, 1348, 1606]  
GOHist000 = [5344, 9439, 10978, 14860, 17326] 

fig, ax1 = plt.subplots()

ax1.set_xlabel('Number of training queries', size  = 14)
ax1.set_xticks(x) 
# ax1.set_yticks([0, 0.03, 0.06, 0.09, 0.12, 0.15])
ax1.plot(x, errorGOHist0, 'cs-', markersize = 8, label = 'RMS Error (0.1)')
ax1.plot(x, errorGOHist00, 'mo-', markersize = 8, label = 'RMS Error (0.01)')
ax1.plot(x, errorGOHist000, 'yv-', markersize = 8, label = 'RMS Error (0.001)')
ax1.tick_params(axis='y', labelsize=14)
ax1.legend(loc = 'upper left', fontsize = 14)
ax1.set_ylim([0,0.16])
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

ax2.set_yscale('log')  # we already handled the x-label with ax1
ax2.plot(x, GOHist0,'cs', linestyle = ':', markersize = 8, label = '#Buckets (0.1)')
ax2.plot(x, GOHist00, 'mo', linestyle = ':', markersize = 8, label = '#Buckets (0.01)')
ax2.plot(x, GOHist000, 'yv', linestyle = ':', markersize = 8, label = '#Buckets (0.001)')
ax2.tick_params(axis='y', labelsize=14)
ax2.set_ylim([1,2000000])
ax2.legend(loc = 'upper right', fontsize =14)
plt.xticks(fontsize=14)

#fig.tight_layout()  # otherwise the rigt y-label is slightly clipped
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14) 
plt.title("Rectangle - Data-aware Workload of Power", fontsize = 14)
plt.tight_layout()
plt.savefig("GOHist-2.pdf")
plt.show()