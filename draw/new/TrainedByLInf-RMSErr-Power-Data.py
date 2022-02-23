import matplotlib.pyplot as plt

# Model Complexity (#buckets)
x = ['0.1k', '0.5k', '1k', '5k', '10k', '50k', '100k']
rmserr_tr50 = [0.128055, 0.041106, 0.066176, 0.103921, 0.045046, 0.120110, 0.052553]
rmserr_tr200 = [0.070665, 0.025270, 0.018694, 0.029941, 0.027756, 0.030171, 0.030027]
rmserr_tr500 = [0.065969, 0.049803, 0.038164, 0.010791, 0.010338, 0.007680, 0.011600]
rmserr_tr1000 = [0.079801, 0.043390, 0.053316, 0.017782, 0.018076, 0.005716, 0.003544]
rmserr_tr2000 = [0.075543, 0.067236, 0.072667, 0.061329, 0.057103, 0.031631, 0.002818]

plt.plot(x, rmserr_tr50, 'yv-', markersize=8, label='m = 50')
plt.plot(x, rmserr_tr200, color='plum', marker='D', markersize=8, label='m = 200')
plt.plot(x, rmserr_tr500, 'bo-', markersize=8, label='m = 500')
plt.plot(x, rmserr_tr1000, 'm*-', markersize=8, label='m = 1000')
plt.plot(x, rmserr_tr2000, 'ks-', markersize=8, label='m = 2000')

plt.xlabel('Model complexity (#buckets)', fontsize=14)
plt.ylabel('RMS error (Test)', fontsize=14)
# plt.xscale('log')
plt.xticks(x, x, fontsize=14)
plt.yticks(fontsize=14)
plt.ylim(0.000, 0.3)
plt.title("Orthogonal - Data-Driven Workload - Power", fontsize=14)
plt.legend(loc='upper right', title='m: training size', title_fontsize=14, fontsize=14)
plt.savefig('TrainedByLInf-RMSErr-Power-Data.pdf')
plt.show()
