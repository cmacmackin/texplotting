#TeXPlots

This is a collection of helper functions for producing good plots to go
into LaTeX files. There is also a LaTeX file to import which imports the
necessary plotting libraries and defines some useful macros.

Using this with Python to create a plot is really easy. Run `pip install .`
from within the repository directory to place the `texplotting` module in
the PYTHONPATH (you may want to use a virtualenv). It can then be imported
into a script and used as follows.

```python
import numpy as np
import matplotlib.pyplot as plt
from texplotting import savetex

x = np.linspace(-1,1,1000)
plt.plot(x, x**2 * sin(0.2/(2.0*np.pi)*x))
savetex('example-plot')
```

This will create both a PGF version of the plot, in `example-plot.pgf`, and
a PDF version of the graph, in `example-plot.pdf`.
To add this plot to a LaTeX document, place a copy of `defaults.tex` in
the directory of said document and put `\include{defaults}` in the preamble.
The following block would then import the figure:

```latex
\begin{figure}
    \includeplot[0.8]{path/to/example-plot}
    \caption{It's as simple as that!}
    \label{fig:example}
\end{figure}
```

The syntax for `includeplot{}` is
```latex
\includeplot[<scale>][<dir>]{<dir>/example-plot}
```
where `<scale>` is the ammount by which to scale the plot size and `<dir>`
is the directory containing the plot. It only needs to be specified as an
optional argument for plots where the PGF imports a PNG file (such as a 2D
colourmap). It defaults to the current directory. The
size of the text in the plot can be adjusted with the use of the appropriate
macro (e.g. `\small`, `\Large`, etc.) prior to the `\includeplot` statement.
If you want to adjust the size of individual text elements in the plot then
include the appropriate macro when setting that text in Python.

Note that previously there was a version of this repository which was based
around `matplotlib2tikz`. However, that library proved problematic when
dealing with more complex graphs. As such, the switch was made to the more
reliable `pgf` backend of `matplotlib`. 
