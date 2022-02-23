import numpy as np
import matplotlib.pyplot as plt

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    if not ax:
        ax = plt.gca()
    im= ax.imshow(data, **kwargs)
    #cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    #cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom", fontsize = 14)
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)
    ax.tick_params(top=False, bottom=True, labeltop=False, labelbottom=True)
    ax.spines[:].set_visible(False)
    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)
    return im#, cbar

x = ["(0.2, 0.2)", "(0.3, 0.3)", "(0.4, 0.4)", "(0.5, 0.5)", "(0.6, 0.6)", "(0.7, 0.7)"]
# y = ["(0.2, 0.2)", "(0.3, 0.3)", "(0.4, 0.4)", "(0.5, 0.5)"]
y = ["(0.7, 0.7)", "(0.6, 0.6)", "(0.5, 0.5)", "(0.4, 0.4)", "(0.3, 0.3)", "(0.2, 0.2)"]

err= np.array([
    [0.087344, 0.191843, 0.097853, 0.074771, 0.002478, 0.000553],
    [0.080242, 0.257239, 0.124469, 0.098002, 0.000598, 0.000349],
    [0.026037, 0.016908, 0.006796, 0.004157, 0.000849, 0.000711], 
    [0.036352, 0.020474, 0.007747, 0.00445, 0.000757, 0.000511],
    [0.013468, 0.007524, 0.011318, 0.011106, 0.018489, 0.009218],
    [0.014919, 0.015648, 0.035068, 0.031966, 0.011652, 0.003791]
    ])
log_err = np.log(err)

fig, ax = plt.subplots()
im = heatmap(log_err, x, y, ax = ax, cmap = "YlGn", cbarlabel = "RMS error")
ax.set_xticks(np.arange(len(x)))
ax.set_yticks(np.arange(len(y)))
ax.set_xlabel("Training query workload", fontsize = 14)
ax.set_ylabel("Test query workload", fontsize = 14)
ax.set_xticklabels(x)
ax.set_yticklabels(y)


for i in range(len(x)):
    for j in range(len(y)):
        text = ax.text(j, i, np.round(err[i, j], 4),
                       ha="center", va="center", color="black")

ax.set_title("Orthogonal - Gaussian - Power")
#ax.set_yticks(rotation='vertical')
fig.tight_layout()
plt.savefig('Mixture-Gaussian.pdf', bbox_inches='tight',dpi=fig.dpi,pad_inches=0.0)
plt.show()
