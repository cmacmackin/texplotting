#TeXPlots

This is a collection of helper functions for producing good plots to go
into LaTeX files. There is also a LaTeX file to import which imports the
necessary plotting libraries and defines some useful macros.

Using this with Python to create a plot is really easy.
```python
import numpy as np
import matplotlib.pyplot as plt
from texplotting import texsave

x = np.linspace(-1,1,1000)
plt.plot(x, x**2 * sin(0.2/(2.0*np.pi)*x))
texsave('example-plot')
```
This will create both a pgfplot, in `example-plot.tex`, and a PDF,
in `example-plot.pdf`, version of the graph.
To add this plot to a LaTeX document, place a copy of `defaults.tex` in
the directory of said document and put `\include{defaults}` in the preamble.
The following block would then import the figure:

```latex
\begin{figure}
    \label{fig:example}
    \includeplot[0.8\textwidth][1.5cm][1.5cm]{path/to/example-plot}
    \caption{It's as simple as that!}
\end{figure}
```

The syntax for `includeplot{}` is
```latex
\includeplot[<figure width>][<horizontal spacing>][<vertical spacing>]{path/to/example-plot}
```
where 

-`<figure width>` is the total width of the figure, defaulting to `\textwidth`
-`<horizontal spacing>` is the horizontal separation between plots if there
 is more than one subplot present, defaulting to `1cm`
-`<horizontal spacing>` is the vertical separation between plots if there
 is more than one subplot present, defaulting to `1cm`.
