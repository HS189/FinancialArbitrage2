import numpy as np  
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt


all_error = np.load("all_error.npy")
c = []
for i in range(0, 5):
	tot = []
	for j in range(0, 4):
		for k in range(0, 4):
			a = all_error[i][j][k]
			for b in a:
				tot.append(b)

	c.append(tot)


a5_mean = np.mean(c[0])
a5_std = np.std(c[0])
a10_mean = np.mean(c[1])
a10_std = np.std(c[1])
a20_mean = np.mean(c[2])
a20_std = np.std(c[2])
a25_mean = np.mean(c[3])
a25_std = np.std(c[3])
a50_mean = np.mean(c[4])
a50_std = np.std(c[4])
print(a5_mean)
print(a10_mean)
print(a20_mean)
print(a25_mean)
print(a50_mean)
currency = ["5", "10", "20", "25", "50"]
x_pos = np.arange(len(currency))
CTEs = [a5_mean, a10_mean, a20_mean, a25_mean, a50_mean]
error = [a5_std, a10_std, a20_std, a25_std, a50_std]

fig, ax = plt.subplots()
ax.bar(x_pos, CTEs, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('Average Error')
ax.set_ylabel('Number of Clusters')
ax.set_xticks(x_pos)
ax.set_xticklabels(currency)
ax.set_title('Average Error with Different Cluster Size')
ax.yaxis.grid(True)

        # Save the figure and show
plt.tight_layout()
plt.savefig("cluster.png")


