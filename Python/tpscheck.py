import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

file = open("tps.txt", "r")

ax = plt.gca()
x = []
y = []

for line in file.read().split("\n"):
    if line == "": break
    r = line.split(" ")
    x.append(int(r[0])/12)
    y.append(float(r[1]))


ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(MultipleLocator(1))

ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_minor_locator(AutoMinorLocator(4))


ax.grid(which='major', color='#CCCCCC', linestyle='solid')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')

plt.xlim(0, 24)
plt.ylim(15, 20)

plt.xlabel("X - Temps en heures")
plt.ylabel("Y - TPS")

plt.plot(x, y)
plt.show()