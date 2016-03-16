from matplotlib2tikz import save as tikz_save
import matplotlib as mpl

def texsave(filename,
         figure='gcf',
         encoding=None,
         textsize=10.0,
         tex_relative_path_to_data=None,
         strict=True,
         draw_rectangles=False,
         wrap=True,
         scale=False,
         times_sci_notation=True,
         extra=set([]),
         show_info=False
         ):
    '''
    Provides a wrapper for saving matplotlib figures in the pgfplot
    format. This makes it easy to import them into LaTeX with native-
    looking text. To do so, place the accompanying ``defaults.tex``
    file in the same directory as your document and include the 
    following in the preamble:
    
    .. code-block:: latex
       \input{defaults}
    
    The plot can then be included as follows:
    
    .. code-block:: latex
       \begin{figure}
         \label{fig:example}
         \setfig{<desired width of plot>}
         \input{<path to file containing plot>}
         \caption{Congratulations! You've added a lovely pgfplot to your
                  \LaTeX document.}
       \end{figure}
    
    :param figure: either a Figure object or 'gcf' (default).
    :param filename: The base name for the files to which the output will be
                     written. No extension should be provided.
    :type filepath: str
    :param encoding: Which encoding to use for the file.
    :param textsize: The text size (in pt) that the target latex document is
                     using.  Default is 10.0. Only affects things like line
                     width.
    :type textsize: float
    :param tex_relative_path_to_data: In some cases, the TikZ file will have to
                                      refer to another file, e.g., a PNG for
                                      image plots. When ``\\input`` into a
                                      regular LaTeX document, the additional
                                      file is looked for in a folder relative
                                      to the LaTeX file, not the TikZ file.
                                      This arguments optionally sets the
                                      relative path from the LaTeX file to the
                                      data.
    :type tex_relative_path_to_data: str
    :param strict: Whether or not to strictly stick to matplotlib's appearance.
                   This influences, for example, whether tick marks are set
                   exactly as in the matplotlib plot, or if TikZ/PGFPlots
                   can decide where to put the ticks.
    :type strict: bool
    :param draw_rectangles: Whether or not to draw Rectangle objects.
                            You normally don't want that as legend, axes, and
                            other entities which are natively taken care of by
                            PGFPlots are represented as rectangles in
                            matplotlib. Some plot types (such as bar plots)
                            cannot otherwise be represented though.
                            Don't expect working or clean output when using
                            this option.
    :type draw_rectangles: bool
    :param wrap: Whether ``'\\begin{tikzpicture}'`` and
                 ``'\\end{tikzpicture}'`` will be written. One might need to
                 provide custom arguments to the environment (eg. scale= etc.).
                 Default is ``True``.
    :type wrap: bool
    :param scale: Whether to allow pgfplot to scale the values on the tick
                  labels for you.
    :type scale: bool
    :param times_sci_notation: Whether to use ``\times`` rather than 
                               ``\cdot`` in any scientific notation on the
                               tick labels.
    :type scale: bool
    :param extra: Extra axis options to be passed (as a set) to pgfplots.
                  Default is ``None``.
    
    :type extra: a set of strings for the pfgplots axes.
    :returns: None
    
    '''
    extra_statements = set(extra)
    if not scale: extra_statements.add('scaled y ticks = false')
    if times_sci_notation:
        extra_statements.add(r'yticklabel={'
                               r'\pgfmathprintnumber['
                                 r'sci generic={'
                                   r'mantissa sep=\times,'
                                   r'exponent={10^{##1}}'
                                 r'}'
                               r']{\tick}'
                             r'}')
    
    # Produce a pgfplot figure in a TeX file
    texpath = filename + '.tex'
    tikz_save(texpath, figure=figure, figurewidth='\\figurewidth',
              figureheight=None, textsize=textsize,
              tex_relative_path_to_data=tex_relative_path_to_data,
              strict=strict, draw_rectangles=draw_rectangles, wrap=wrap,
              show_info=show_info, extra=extra_statements)
    
    # Create a standalone PDF figure for immediate analysis
    if figure == 'gcf': 
        figure = mpl.pyplot.gcf()
    pdfpath = filename + '.pdf'
    figure.savefig(pdfpath)

