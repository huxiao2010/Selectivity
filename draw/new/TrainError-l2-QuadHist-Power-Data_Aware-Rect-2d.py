import matplotlib.pyplot as plt

# Model Complexity (#buckets)

x = ['0.1k', '0.5k', '1k', '5k', '10k', '50k', '100k']
QuadHist_tr50 = [0.02828,
                 0.000807,
                 4.00E-06,
                 0,
                 0,
                 0,
                 0]
QuadHist_tr200 = [0.031256,
                  0.006334,
                  0.002794,
                  0.000856,
                  0.000606,
                  0.000248,
                  0]
QuadHist_tr500 = [0.041416,
                  0.011394,
                  0.006029,
                  0.001283,
                  0.000844,
                  0.000429,
                  0.000235]
QuadHist_tr1000 = [0.023397,
                   0.010787,
                   0.009021,
                   0.002836,
                   0.002814,
                   0.000594,
                   0.000263]
QuadHist_tr2000 = [0.027074,
                   0.012985,
                   0.011709,
                   0.005476,
                   0.005445,
                   0.003293,
                   0.000297]

plt.plot(x, QuadHist_tr50, 'yv-', markersize=8, label='m = 50')
plt.plot(x, QuadHist_tr200, color='plum', marker='D', markersize=8, label='m = 200')
plt.plot(x, QuadHist_tr500, 'bo-', markersize=8, label='m = 500')
plt.plot(x, QuadHist_tr1000, 'm*-', markersize=8, label='m = 1000')
plt.plot(x, QuadHist_tr2000, 'ks-', markersize=8, label='m = 2000')

plt.xlabel('Model complexity (#buckets)', fontsize=14)
plt.ylabel('RMS error (Train)', fontsize=14)
# plt.xscale('log')
plt.xticks(x, x, fontsize=14)
plt.yticks(fontsize=14)
plt.ylim(0.000, 0.15)
plt.title("Orthogonal - Data-Driven Workload - Power", fontsize=14)
plt.legend(loc='upper right', title='m: training size', title_fontsize=14, fontsize=14)
plt.savefig('Starter-TrainError-L2-QuadHist-Power-Data_Aware-Rect-2d.pdf')
plt.show()
