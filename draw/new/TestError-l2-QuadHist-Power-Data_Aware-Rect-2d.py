import matplotlib.pyplot as plt

# Model Complexity (#buckets)
x = ['0.1k', '0.5k', '1k', '5k', '10k', '50k', '100k']
QuadHist_tr50 = [0.036878,
                 0.021109,
                 0.028236,
                 0.027225,
                 0.039783,
                 0.05099,
                 0.052566]
QuadHist_tr200 = [0.053482,
                  0.026421,
                  0.018701,
                  0.039016,
                  0.039037,
                  0.04919,
                  0.047949]
QuadHist_tr500 = [0.052499,
                  0.020069,
                  0.014923,
                  0.008958,
                  0.009707,
                  0.011639,
                  0.012781]
QuadHist_tr1000 = [0.032025,
                   0.014691,
                   0.013549,
                   0.008562,
                   0.008615,
                   0.004074,
                   0.002401]
QuadHist_tr2000 = [0.030574,
                   0.014375,
                   0.013499,
                   0.008228,
                   0.008276,
                   0.003843,
                   0.000958]

plt.plot(x, QuadHist_tr50, 'yv-', markersize=8, label='m = 50')
plt.plot(x, QuadHist_tr200, color='plum', marker='D', markersize=8, label='m = 200')
plt.plot(x, QuadHist_tr500, 'bo-', markersize=8, label='m = 500')
plt.plot(x, QuadHist_tr1000, 'm*-', markersize=8, label='m = 1000')
plt.plot(x, QuadHist_tr2000, 'ks-', markersize=8, label='m = 2000')

plt.xlabel('Model complexity (#buckets)', fontsize=14)
plt.ylabel('RMS error (Test)', fontsize=14)
# plt.xscale('log')
plt.xticks(x, x, fontsize=14)
plt.yticks(fontsize=14)
plt.ylim(0.000, 0.15)
plt.title("Orthogonal - Data-Driven Workload - Power", fontsize=14)
plt.legend(loc='upper right', title='m: training size', title_fontsize=14, fontsize=14)
plt.savefig('Starter-TestError-L2-QuadHist-Power-Data_Aware-Rect-2d.pdf')
plt.show()
