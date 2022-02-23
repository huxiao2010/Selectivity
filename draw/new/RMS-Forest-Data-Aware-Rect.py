import matplotlib.pyplot as plt

x = [50, 200, 500, 1000, 2000]

PtsHist2 = [0.08038, 0.01168, 0.00408, 0.00213, 0.00149]
PtsHist4 = [0.08078, 0.01622, 0.00858, 0.00589, 0.00492]
PtsHist6 = [0.05722, 0.02575, 0.01393, 0.00722, 0.0054]
PtsHist8 = [0.04614, 0.03834, 0.02405, 0.02252, 0.02504]
PtsHist10 = [0.08354, 0.07645, 0.05475, 0.04828, 0.05471]

# QuadHist2  = [0.09969, 0.061317, 0.005235, 0.004517, 0.001444]
# QuadHist4 = [0.066463, 0.050599, 0.038423, 0.007306, 0.006499]
# QuadHist6 = [0.062077, 0.045007, 0.016212, 0.012465, 0.010358]

plt.plot(x, PtsHist2,  color = 'k', marker = '*', markersize = 8, label = 'PtsHist (d=2)')
plt.plot(x, PtsHist4,  color = 'indigo', marker = 'P', markersize = 8, label = 'PtsHist (d=4)')
plt.plot(x, PtsHist6,  color = 'blueviolet', marker = 'X', markersize = 8, label = 'PtsHist (d=6)')
plt.plot(x, PtsHist8,  color = 'mediumorchid', marker = 'D', markersize = 8, label = 'PtsHist (d=8)')
plt.plot(x, PtsHist10, color = 'plum', marker = 's', markersize = 8, label = 'PtsHist (d=10)')

# plt.plot(x, QuadHist2, color = '#159f49', marker = '*', markersize = 8, label = 'QuadHist (d=2)')
# plt.plot(x, QuadHist4, color = '#5fedcf', marker = 'P', markersize = 8, label = 'QuadHist (d=4)')
# plt.plot(x, QuadHist6, color = '#fff308', marker = 'X', markersize = 8, label = 'QuadHist (d=6)')

plt.xlabel('Number of training queries', fontsize = 14)
plt.ylabel('RMS error', fontsize = 14)
plt.xticks(x, fontsize = 14)
plt.yticks(fontsize = 14)
plt.title("Orthogonal - Data-Driven Workload - Forest", fontsize =14)
plt.legend(loc = 'upper right', fontsize= 12, ncol = 2)
plt.savefig('RMS-Forest-Data-Aware-Rect.pdf')
plt.show()
