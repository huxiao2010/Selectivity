
import matplotlib
import matplotlib.pyplot as plt
import random
  

k = 100
  
fig = plt.figure()
ax = fig.add_subplot(111)

rect = [[] for i in range(k)]


for i in range(k):
	x = random.uniform(0,2.65)
	y = random.uniform(0,1.85)
	length = random.uniform(0,2.65 - x)
	width = random.uniform(0,1.85- y)
	print(str(x) + ' ' + str(y) + ' ' + str(length) + ' ' + str(width) + ' ' + str(i) + '\n')
	rect[i] = matplotlib.patches.Rectangle((x,  y), length, width, fill = None, linewidth = 0.5)
	ax.add_patch(rect[i])

#ax.get_xaxis().set_visible(False)
#ax.get_yaxis().set_visible(False)
plt.xlim(0,2.65)
plt.ylim(0,1.85)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
plt.savefig("random-workload.png") 
  
plt.show()