import matplotlib.pyplot as plt

# Model Complexity (#buckets)
x = ['0.1k', '0.5k', '1k', '5k', '10k', '50k', '100k']
trainerr_tr50 = [0.089705, 0.002332, 0.000614, 0.000000, 0.000000, 0.000000, 0.000000]
trainerr_tr200 = [0.137124, 0.019522, 0.010802, 0.004014, 0.003066, 0.001406, 0.000001]
trainerr_tr500 = [0.149339, 0.090310, 0.047396, 0.006371, 0.005809, 0.003526, 0.002228]
trainerr_tr1000 = [0.188117, 0.097464, 0.097324, 0.026220, 0.026209, 0.003940, 0.003042]
trainerr_tr2000 = [0.220012, 0.185309, 0.185309, 0.135589, 0.135052, 0.071638, 0.003256]

plt.plot(x, trainerr_tr50, 'yv-', markersize=8, label='m = 50')
plt.plot(x, trainerr_tr200, color='plum', marker='D', markersize=8, label='m = 200')
plt.plot(x, trainerr_tr500, 'bo-', markersize=8, label='m = 500')
plt.plot(x, trainerr_tr1000, 'm*-', markersize=8, label='m = 1000')
plt.plot(x, trainerr_tr2000, 'ks-', markersize=8, label='m = 2000')

plt.xlabel('Model complexity (#buckets)', fontsize=14)
plt.ylabel('LInf error (Train)', fontsize=14)
# plt.xscale('log')
plt.xticks(x, x, fontsize=14)
plt.yticks(fontsize=14)
plt.ylim(0.000, 0.3)
plt.title("Orthogonal - Data-Driven Workload - Power", fontsize=14)
plt.legend(loc='upper right', title='m: training size', title_fontsize=14, fontsize=14)
plt.savefig('TrainedByLInf-TrainingErr-Power-Data.pdf')
plt.show()
