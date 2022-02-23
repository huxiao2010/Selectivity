import matplotlib.pyplot as plt

# Model Complexity (#buckets)
x = [100, 500, 1000, 5000, 10000]
QuadHist_tr50 = [0.073, 0.057, 0.04, 0.026, 0.036]
QuadHist_tr200 = [0.036, 0.017, 0.016, 0.014, 0.013] 
QuadHist_tr500 = [0.035, 0.013, 0.009, 0.0059, 0.0045]
QuadHist_tr1000 = [0.0185, 0.009, 0.0081, 0.0035, 0.0039]
QuadHist_tr2000 = [0.0198, 0.0079, 0.0058, 0.0033, 0.0033]

plt.plot(x, QuadHist_tr50,'yv-', markersize = 8, label = 'm = 50')
plt.plot(x, QuadHist_tr200, color = 'plum', marker = 'D', markersize = 8, label = 'm = 200')
plt.plot(x, QuadHist_tr500, 'bo-', markersize = 8, label = 'm = 500')
plt.plot(x, QuadHist_tr1000, 'm*-', markersize = 8, label = 'm = 1000')
plt.plot(x, QuadHist_tr2000, 'ks-', markersize = 8, label = 'm = 2000')

plt.xlabel('Model complexity (#buckets)', fontsize = 14)
plt.ylabel('RMS error', fontsize = 14)
plt.xscale('log')
plt.xticks(x, x, fontsize = 14)
plt.yticks(fontsize = 14)
plt.title("Orthogonal - Data-Driven Workload - Power", fontsize = 14)
plt.legend(loc = 'upper right', title = 'm: training size', title_fontsize = 14, fontsize =14)
plt.savefig('Starter-QuadHist-Power-Data_Aware-Rect-2d.pdf')
plt.show()





