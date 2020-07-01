import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

maxram = 8594128896
ramgo = 8

file = open("ram.txt", "r")

ax = plt.gca()
x = []
y = []

for line in file.read().split("\n"):
    if line == "": break
    r = line.split(" ")
    x.append(int(r[0])/12)
    y.append(int(r[1])*ramgo/maxram)


ax.xaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_locator(MultipleLocator(1))

ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_minor_locator(AutoMinorLocator(4))


ax.grid(which='major', color='#CCCCCC', linestyle='solid')
ax.grid(which='minor', color='#CCCCCC', linestyle=':')

plt.xlim(0, 24)
plt.ylim(0, ramgo)

plt.xlabel("X - Temps en heures")
plt.ylabel("Y - RAM utilisée")

plt.plot(x, y)
plt.show()