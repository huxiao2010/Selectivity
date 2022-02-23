
import matplotlib
import matplotlib.pyplot as plt
import random
  

k = 100
  
fig = plt.figure()
ax = fig.add_subplot(111)

rect = [[] for i in range(k)]


for i in range(k):
	x = random.gauss(0.5, 0.15)
	y = random.gauss(0.5, 0.15)
	length = random.uniform(0,0.1)

	width = random.uniform(0,0.1)

	rect[i] = matplotlib.patches.Rectangle((x,  y), length, width, fill = None)
	ax.add_patch(rect[i])



ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)

plt.savefig("../results/pic/f7/gauss-workload.pdf")
  
# plt.show()