import latexplotlib as lpl
import numpy as np

lpl.style.use("latex10pt-minimal")
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
fig.savefig("example_poly_minimal")
fig.savefig("example_poly_minimal.png")
