import matplotlib.pyplot as plt

# Model Complexity (#buckets)

x = ['0.1k', '0.5k', '1k', '5k', '10k', '50k', '100k']
QuadHist_tr50 = [0.21513,
                 0.026419,
                 0.000293,
                 0.00E+00,
                 0.00E+00,
                 0.00E+00,
                 0.00E+00]
QuadHist_tr200 = [0.16247,
                  0.066378,
                  0.075956,
                  0.006919,
                  0.006663,
                  0.005287,
                  0.002118]
QuadHist_tr500 = [0.175407,
                  0.080196,
                  0.08564,
                  0.026511,
                  0.025608,
                  0.006465,
                  0.006241]
QuadHist_tr1000 = [0.103916,
                   0.107147,
                   0.107461,
                   0.050961,
                   0.028312,
                   0.015788,
                   0.006189]
QuadHist_tr2000 = [0.210085,
                   0.154536,
                   0.155186,
                   0.072599,
                   0.049748,
                   0.020671,
                   0.005789]

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
plt.title("Orthogonal - Data-Driven Workload - Power", fontsize=14)
plt.legend(loc='upper right', title='m: training size', title_fontsize=14, fontsize=14)
plt.savefig('Starter-TrainError-Linf-QuadHist-Power-Data_Aware-Rect-2d.pdf')
plt.show()
