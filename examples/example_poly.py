import matplotlib.pyplot as plt
import numpy as np

plt.style.use("latex10pt")

x = np.linspace(1, 5, 100)

for t in range(4):
    label = f"$x^{t}$"
    plt.plot(x, x ** t, label=label)

plt.yscale("log")
plt.title("Perfect matplotlib figures for \\LaTeX")
plt.grid()
plt.legend()
plt.tight_layout()

plt.savefig("example_poly")
plt.savefig("example_poly.png")
