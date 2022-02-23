import matplotlib.pyplot as plt

# Model Complexity (#buckets)
x = ['0.1k', '0.5k', '1k', '5k', '10k', '50k', '100k']
QuadHist_tr50 = [0.225708,
                 0.212587,
                 0.221627,
                 0.224067,
                 0.249698,
                 0.310632,
                 0.288033]
QuadHist_tr200 = [0.262617,
                  0.208614,
                  0.202181,
                  0.228954,
                  0.225124,
                  0.245032,
                  0.244151]
QuadHist_tr500 = [0.246259,
                  0.212211,
                  0.200063,
                  0.171988,
                  0.173086,
                  0.189071,
                  0.187818]
QuadHist_tr1000 = [0.22514,
                   0.204699,
                   0.203578,
                   0.170345,
                   0.170416,
                   0.109648,
                   0.019977]
QuadHist_tr2000 = [0.224878,
                   0.205865,
                   0.208096,
                   0.170527,
                   0.170566,
                   0.109028,
                   0.009287]

plt.plot(x, QuadHist_tr50, 'yv-', markersize=8, label='m = 50')
plt.plot(x, QuadHist_tr200, color='plum', marker='D', markersize=8, label='m = 200')
plt.plot(x, QuadHist_tr500, 'bo-', markersize=8, label='m = 500')
plt.plot(x, QuadHist_tr1000, 'm*-', markersize=8, label='m = 1000')
plt.plot(x, QuadHist_tr2000, 'ks-', markersize=8, label='m = 2000')

plt.xlabel('Model complexity (#buckets)', fontsize=14)
plt.ylabel('Linf error (Test)', fontsize=14)
# plt.xscale('log')
plt.ylim(0.000, 0.6)
plt.xticks(x, x, fontsize=14)
plt.yticks(fontsize=14)
plt.title("Orthogonal - Data-Driven Workload - Power", fontsize=14)
plt.legend(loc='upper right', title='m: training size', title_fontsize=14, fontsize=14)
plt.savefig('Starter-TestError-Linf-QuadHist-Power-Data_Aware-Rect-2d.pdf')
plt.show()
