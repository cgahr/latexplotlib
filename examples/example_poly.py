import matplotlib.pyplot as plt
import numpy as np

import latexplotlib as lpl

plt.style.use("latex10pt")

# lpl.size.set(200, 400)
with lpl.size.context(200, 400):
    fig, ax = lpl.subplots(1, 1)

x = np.linspace(1, 5, 100)

for t in range(4):
    label = f"$x^{t}$"
    ax.plot(x, x**t, label=label)

ax.set_yscale("log")
ax.set_title("Perfect matplotlib figures for \\LaTeX")
ax.grid()

fig.legend()
fig.savefig("example_poly")
fig.savefig("example_poly.png")
