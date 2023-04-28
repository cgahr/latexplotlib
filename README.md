# latexplotlib

[![image](https://img.shields.io/pypi/v/latexplotlib.svg)](https://pypi.python.org/pypi/latexplotlib)
[![image](https://img.shields.io/pypi/l/latexplotlib.svg)](https://pypi.python.org/pypi/latexplotlib)
[![image](https://img.shields.io/pypi/pyversions/latexplotlib.svg)](https://pypi.python.org/pypi/latexplotlib)
[![Actions status](https://github.com/cgahr/latexplotlib/actions/workflows/main.yml/badge.svg)](https://github.com/cgahr/latexplotlib/actions)
[![Coverage Status](https://coveralls.io/repos/github/cgahr/latexplotlib/badge.svg?branch=main)](https://coveralls.io/github/cgahr/latexplotlib?branch=main)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)

Perfect matplotlib figures for latex.


## Quickstart

1. install `latexplotlib`:
```python
pip install latexplotlib
```
2. import latexplotlib and use latexplotlib style
```python
import latexplotlib as lpl

plt.style.use('latex10pt')
# lpl.style.use('latex10pt-minimal')
```

3. replace all `plt.subplots` with `lpl.subplots`:
```python
#  fig, axes = plt.subplots(2, 3)
fig, axes = lpl.subplots(2, 3)
```

Optional:

4. get size of latex document
```latex
(\the\textwidth, \the\textheight)  % (412.123pt, 346.564pt)
```
5. set `lpl.size` to size of latex document
```python
lpl.size.set(412.123, 346.564)
```

## Usage

This package has two basic functionalities. On the one hand, it sets sensible defaults
for creating perfect figures for latex. This includes a color scheme optimized for
color-blind people, correct font and font sizes, and sensible defaults to store the
figure. On the other hand, it provides some functions to create perfectly sized figures.
These figures fit your latex document without scaling and have the correct font size for
your document.

### latexplotlib styles

There are 6 different styles for matplotlib:

- `latex10pt-minimal`
- `latex11pt-minimal`
- `latex12pt-minimal`
- `latex10pt`
- `latex11pt`
- `latex12pt`

The `*minimal` versions change the font and the font sizes to ensure that the figures fonts match the latex font. This style is fully compatible with other styles:

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


The non-minimal versions set additional defaults to create figures that are accessible for color-blind people:

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

Both styles change the defaults of the `plt.savefig` command. The new defaults are

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

### Get latex dimensions
You can find the width and height of your document using the following command:

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
_ = lpl.subplots(1, 1)

# A subplot filling 80% of the latex page
fig, axes = lpl.subplots(3, 2, scale=0.8)

# A subplot for 3 square plots next to each other
fig, axes = lpl.subplots(1, 3, scale=0.8, aspect='equal')
```

### `aspect` keyword
The `aspect` keyword controls the ratio of height to width. The default is the Golden ratio. `aspect` can also be `equal` (i.e. `aspect=1` )or `auto`. In the latter case, the figure fills the available space.

```python
import matplotlib.pyplot as plt

import latexplotlib as lpl

# A 3 by 2 figure where each subplots height to width ratio is the golden ratio
fig, axes = lpl.subplots(3, 2)

# A 3 by 2 figure where each subplot having a height to width ratio of 1:1
fig, axes = lpl.subplots(3, 2, aspect=1.0)

# A figure that is exactly 300pt height and 200pt wide
with lpl.size.context(200, 300):
    fig, axes = lpl.subplots(3, 2, aspect="auto")
```


### Include figures in Latex

The most important part of including the figures in latex is to not set the size of the figure using arguments like `[width=...]`:
```latex
\includegraphics[width=\textwidth]{test.pdf}
```

Instead, latexplotlib creates figures that are already properly sized. As such, figure can be added using only
```latex
\includegraphics}{test.pdf}
```

### `plt.tight_layout()`

`plt.tight_layout()` changes the size of the produced figure. As such it is recommended to not use `plt.tight_layout()` with care! The same is true for `savefig(..., bbox_inches=None)`!

Instead all latexplotlib styles used `constrained_layout` by default. `constrained_layout` has a similar functionality compared to `tight_layout`, however it is fully deterministic and does not change the size of the underlying figure.

## References

This package is inspired by the following sources:

- Code: https://pypi.org/project/SciencePlots/
- Figure sizes: https://jwalton.info/Embed-Publication-Matplotlib-Latex/
- Color palette (Okabe Ito): https://clauswilke.com/dataviz/color-basics.html
