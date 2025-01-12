import random


import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#define Matplotlib figure and axis
fig, ax = plt.subplots()

#create simple line plot
ax.plot([0, 10],[0, 10])

#add rectangle to plot
r = Rectangle((1, 1), 2, 6,)
ax.add_patch(r)
ax.text(r.get_center()[0], r.get_center()[1], 'Hello', horizontalalignment = 'center', verticalalignment = 'center')

# Enable grid lines
ax.grid()
# ax.invert_xaxis()
ax.invert_yaxis()

#display plot
plt.show()