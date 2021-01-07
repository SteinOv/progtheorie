import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


fig = plt.figure()
ax = plt.axes()

x = [1,6,10,15,3,12,14,1,6,12,15,2,8,1,4,10,11,16,2,7,10,12,15,6,13,16,6,7]
y = [15,15,15,15,14,14,14,13,13,13,13,12,12,11,11,11,11,11,10,10,10,10,10,9,9,9,8,8]

ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(MultipleLocator(1))

ax.scatter(x, y)

plt.grid()
plt.show()
