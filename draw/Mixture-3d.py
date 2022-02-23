import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Construct arrays for the anchor positions of the 16 bars.
xpos = []
ypos = []
for x in np.arange(-0.0625, 1.0, 0.25):
    for y in np.arange(-0.0625, 1.0, 0.25):
        xpos.append(x)
        ypos.append(y)

xpos = np.array(xpos).ravel()
ypos = np.array(ypos).ravel()
zpos = 0.0


# Construct arrays with the dimensions for the 16 bars.
dx = dy = 0.240
dz = PTSHist1 = [0.0054234
,0.0049383
,0.004331
,0.0036736
,0.0028321
,0.0022995
,0.0021803
,0.0021558
,0.002148
,0.0021037
,0.0018079
,0.0018788
,0.0019146
,0.0019431
,0.0019582
,0.0016952
,0.0017447
,0.0017941
,0.0017959
,0.0017989
,0.0014609
,0.0016008
,0.0016736
,0.0017706
,0.0018545]

colors = []
for i in range(len(dz)):
    color_z = 1.0
    if dz[i] > 0.0017:
        color_z /= 2
    if dz[i] > 0.0019:
        color_z /= 2
    if dz[i] > 0.003:
        color_z /= 2
    if dz[i] > 0.004:
        color_z /= 2
    colors.append(np.array([1.0, 1 - color_z, 1 - color_z]))
dz = np.array(dz)

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color = colors)

ax.set_xlabel('Training ratio', fontsize = 12)
ax.set_ylabel('Test ratio', fontsize = 12)
ax.set_zlabel('RMS error', fontsize = 12)
plt.xticks([1.0, 0.75, 0.5, 0.25, 0.0], fontsize = 10)
plt.yticks([0.0, 0.25, 0.5, 0.75, 1.0], fontsize = 10)
plt.title("Rectangle - Mixture - Forest", fontsize = 14)
plt.savefig("Mixture-3d.pdf")
plt.show()