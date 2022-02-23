import matplotlib.pyplot as plt

x = [2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 9900]
y = [0.001, 0.002, 0.003]

GOHist = [0.001109, 0.001143, 0.000793, 0.0007, 0.000764, 0.00077, 0.00079, 0.000726, 0.000851]
GOHist2000 = [0.001555, 0.002326, 0.001851, 0.001362, 0.000989]
# 0.003 7000
PtsHist = [0.001562, 0.001177, 0.001682, 0.001388, 0.001781, 0.001795, 0.001699, 0.001695, 0.002218]
PtsHist2000 = [0.001454, 0.002475, 0.001807, 0.001926, 0.001932]
# 0.04 0.1 7000


plt.plot(x, GOHist, 'm.-', markersize = 8, label = 'GOHist')
plt.plot(x, PtsHist, 'b.-', markersize = 8, label = 'PtsHist')

for i in range(len(GOHist2000)):
    plt.scatter(2000, GOHist2000[i], c = 'm', marker = '.', s = 64)
for i in range(len(PtsHist2000)):
    plt.scatter(2000, PtsHist2000[i], c = 'b', marker = '.', s = 64)

plt.xlabel('Number of training queries', fontsize = 14)
plt.ylabel('RMS error', fontsize = 14)
plt.xticks(x, fontsize = 12)
plt.yticks(y, fontsize = 11)
plt.title("Rectangle - Random Workload - Power", fontsize =14)
plt.legend(loc = 'upper right', fontsize= 14)
plt.savefig('Scalability.pdf')
plt.show()
