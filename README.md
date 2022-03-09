# latexplotlib

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

Perfect matplotlib figures for latex.


## Usage

This package has two basic functionalities. On the one hand, it sets sensible defaults
for creating perfect figures for latex. This includes a color scheme optimized for
color-blind people, correct font and font sizes, and sensible defaults to store the
figure. On the other hand, it provides some functions to create perfectly sized figures.
These figures fit your latex document without scaling and have the correct font size for
your document.

### latexplotlib styles

There are 6 different styles for matplotlib.
- `latex10pt`
- `latex11pt`
- `latex12pt`
- `latex10pt-minimal`
- `latex11pt-minimal`
- `latex12pt-minimal`

The `*minimal` versions change the font and the font sizes to ensure that the figures fonts match the latex font perfectly. This style is fully compatible with other styles.

The non-minimal versions set additional defaults to create perfect figures, that are accessible for color-blind people while still looking nice.

Both styles change the defaults of the `plt.savefig` command so that all saved figures look good. These new defaults are

```python
plt.savefig(
    ...,
    bbox_inches=None,
    dpi=300,
    format="pdf",
    orientation="portrait",
    pad_inches=0.05
)
```

### Example

Style `latex10pt`:

```python
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
    ax.plot(x, x ** t, label=label)

ax.set_yscale("log")
ax.set_title("Perfect matplotlib figures for \\LaTeX")
ax.grid()

fig.legend()
fig.savefig("example_poly")
fig.savefig("example_poly.png")
```
<p align="center">
<img src="https://github.com/ConstantinGahr/latexplotlib/blob/main/examples/example_poly.png?raw=true" width="500">
</p>

Style `latex10ptminimal`:
```python
import matplotlib.pyplot as plt
import numpy as np

import latexplotlib as lpl

plt.style.use("latex10pt-minimal")
# lpl.size.set(200, 400)
with lpl.size.context(200, 400):
    fig, ax = lpl.subplots(1, 1)

x = np.linspace(1, 5, 100)

for t in range(4):
    label = f"$x^{t}$"
    ax.plot(x, x ** t, label=label)

ax.set_yscale("log")
ax.set_title("Perfect matplotlib figures for \\LaTeX")
ax.grid()

fig.legend()
plt.savefig("example_poly_minimal")
plt.savefig("example_poly_minimal.png")
```

<p align="center">
<img src="https://github.com/ConstantinGahr/latexplotlib/blob/main/examples/example_poly_minimal.png?raw=true" width="500">
</p>

### Get latex dimensions
You can find the dimensions of your document using the following command:

```latex
\the\textwidth

\the\textheight
```

### Set and get latex page size

```python
import latexplotlib as lpl

lpl.size.set(200, 400)

with lpl.size.context(100, 200):
    lpl.size()  # 100, 200

lpl.size()  # (200, 400)
```

### Create figures for latex
```python
import matplotlib.pyplot as plt

import latexplotlib as lpl


# A figure filling 75% of the latex page
_ = plt.figure(figsize=lpl.figsize(fraction=0.75))

# A subplot filling 80% of the latex page
fig, axes = lpl.subplots(3, 2, fraction=0.8)

# A subplot for 3 square plots next to each other
fig, axes = lpl.subplots(1, 3, fraction=0.8, ratio=1)
```

### `ratio` keyword
The `ratio` keyword control the ratio of height to width. The default is the Golden ratio. `ratio` can also be `max` or `any`. In this case, the figure fills the available space.
```python
import matplotlib.pyplot as plt

import latexplotlib as lpl

# A 3 by 2 figure where each subplots height to width ratio is the golden ratio
fig, axes = lpl.subplots(3, 2)

# A 3 by 2 figure where each subplot having a height to width ratio of 1:1
fig, axes = lpl.subplots(3, 2, ratio=1.0)

# A figure that is exactly 300pt height and 200pt wide
with lpl.size.context(200, 300):
    fig, axes = lpl.subplots(3, 2, ratio"max")
```


### Include figures in Latex
```latex
\begin{figure}[tb]
    \centering
    \includegraphics{test.pdf}
    \caption{A test figure.}
\end{figure}
```

## `plt.tight_layout()`

`plt.tight_layout()` changes the size of the produced figure. As such it is recommended to only use `plt.tight_layout()` with care! The same is true for `savefig(..., bbox_inches=None)`!

Instead one should use `constrained_layout` which produces nice figures. `constrained_layout` is used by default with all latexplotlib styles.

## References

This package is inspired by the following sources:

- Code: https://pypi.org/project/SciencePlots/
- Figure sizes: https://jwalton.info/Embed-Publication-Matplotlib-Latex/
- Color palette (Okabe Ito): https://clauswilke.com/dataviz/color-basics.html
