import matplotlib.pyplot as plt

# Model Complexity (#buckets)
x = ['0.1k', '0.5k', '1k', '5k', '10k', '50k', '100k']
testerr_tr50 = [0.372214, 0.228071, 0.422141, 0.480944, 0.236643, 0.512118, 0.275251]
testerr_tr200 = [0.284209, 0.211736, 0.201081, 0.212709, 0.200244, 0.214326, 0.225606]
testerr_tr500 = [0.344944, 0.209176, 0.193935, 0.173596, 0.174017, 0.132332, 0.191934]
testerr_tr1000 = [0.288791, 0.218047, 0.234436, 0.163332, 0.163215, 0.114271, 0.044144]
testerr_tr2000 = [0.229757, 0.241432, 0.243141, 0.192843, 0.194481, 0.130924, 0.016704]

plt.plot(x, testerr_tr50, 'yv-', markersize=8, label='m = 50')
plt.plot(x, testerr_tr200, color='plum', marker='D', markersize=8, label='m = 200')
plt.plot(x, testerr_tr500, 'bo-', markersize=8, label='m = 500')
plt.plot(x, testerr_tr1000, 'm*-', markersize=8, label='m = 1000')
plt.plot(x, testerr_tr2000, 'ks-', markersize=8, label='m = 2000')

plt.xlabel('Model complexity (#buckets)', fontsize=14)
plt.ylabel('LInf error (Test)', fontsize=14)
# plt.xscale('log')
plt.xticks(x, x, fontsize=14)
plt.yticks(fontsize=14)
plt.ylim(0.000, 1.0)
plt.title("Orthogonal - Data-Driven Workload - Power", fontsize=14)
plt.legend(loc='upper right', title='m: training size', title_fontsize=14, fontsize=14)
plt.savefig('TrainedByLInf-TestErr-Power-Data.pdf')
plt.show()
