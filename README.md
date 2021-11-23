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
    bbox_inches="tight",
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
```
<p align="center">
<img src="https://github.com/ConstantinGahr/latexplotlib/blob/main/examples/example_poly.png?raw=true" width="500">
</p>

Style `latex10ptminimal`:
```python
import matplotlib.pyplot as plt
import numpy as np


plt.style.use("latex10pt-minimal")

x = np.linspace(1, 5, 100)

for t in range(4):
    label = f"$x^{t}$"
    plt.plot(x, x ** t, label=label)

plt.yscale("log")
plt.title("Perfect matplotlib figures for \\LaTeX")
plt.grid()
plt.legend()
plt.tight_layout()

plt.savefig("example_poly_minimal")
```

<p align="center">
<img src="https://github.com/ConstantinGahr/latexplotlib/blob/main/examples/example_poly_minimal.png?raw=true" width="500">
</p>

### Get latex dimensions
You can find the dimensions of your document using the following command:

```latex
\usepackage{layout}

\layout
```
The necessary dimension are found under `\textwidth` and `\textheight`.

### Set and get latex page size

```python
from latexplotlib import set_page_size, get_page_size

# set the page size in pt
set_page_size(630, 412)

get_page_size()
# (630, 412)
```

### Create figures for latex
```python
from latexplotlib as figsize, subplots
import matplotlib.pyplot as plt


# A figure filling 75% of the latex page
_ = plt.figure(figsize=figsize(fraction=0.75))

# A subplot filling 80% of the latex page
fig, axes = subplots(3, 2, fraction=0.8)
```


### Include figures in Latex
```latex
\begin{figure}[tb]
    \centering
    \includegraphics{test.pdf}
    \caption{A test figure.}
\end{figure}
```

## References

This package is inspired by the following sources:

- Code: https://pypi.org/project/SciencePlots/
- Figure sizes: https://jwalton.info/Embed-Publication-Matplotlib-Latex/
- Color palette (Okabe Ito): https://clauswilke.com/dataviz/color-basics.html
