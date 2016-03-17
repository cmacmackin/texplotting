from matplotlib2tikz import save as tikz_save
import matplotlib as mpl
import re

GROUP_RE = re.compile(r'(group\s+style\s*=\s*\{(?:[^}]+,)*?''\s*group\s+'
                      r'size\s*=\s*\d+\s+by\s+\d+(?:,[^}]+)*?)\}')
GROUP_ADD = r'\1, horizontal sep=\xsepwidth, vertical sep=\ysepwidth}'

def texsave(filename,
         figure='gcf',
         encoding=None,
         textsize=10.0,
         tex_relative_path_to_data=None,
         strict=True,
         strict_labels=True,
         draw_rectangles=False,
         wrap=True,
         scale=False,
         times_sci_notation=True,
         exp_cutoff = (-4,4),
         precision = 3,
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
         \includeplot[<width>]{<path to file containing plot>}
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
    :param strict_labels: If ``strict == True``, whether to strictly adhere
                          to matplotlib's labels or whether to have pgfplot
                          create them itself, with the style modified according
                          to the specifications given in other arguments.
    :type strict_labels: bool
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
    :param exp_cutoff: The lower and upper bounds for the exponent of a number
                       beyond which scientific notation is used. If the number
                       is within these bounds (inclusive) then a floating point
                       number is used.
    :type exp_cutoff: (int, int)
    :param extra: Extra axis options to be passed (as a set) to pgfplots.
                  Default is ``None``.
    :param precision: The number of decimal places to show.
    :type precision: int
    :type extra: a set of strings for the pfgplots axes.
    :returns: None
    
    '''
    extra_statements = set(extra)
    if not scale or strict_labels:
        extra_statements.add('scaled y ticks = false')
        extra_statements.add('scaled x ticks = false')
    if times_sci_notation and not strict_labels:
        extra_statements.add(r'xticklabel={'
                               r'\pgfmathprintnumber['
                                 r'relative*={%i},relative style={std=%i:%i},'
                                  r'sci generic={'
                                   r'mantissa sep=\times,'
                                   r'exponent={10^{##1}}'
                                 r'},'
                                 r'precision={%i}'
                               r']{\tick}'
                             r'}' % (exp_cutoff[0], exp_cutoff[0],
                                     exp_cutoff[1], precision))
        extra_statements.add(r'yticklabel={'
                               r'\pgfmathprintnumber['
                                 r'relative*={%i},relative style={std=%i:%i},'
                                  r'sci generic={'
                                   r'mantissa sep=\times,'
                                   r'exponent={10^{##1}}'
                                 r'},'
                                 r'precision={%i}'
                               r']{\tick}'
                             r'}' % (exp_cutoff[0], exp_cutoff[0],
                                     exp_cutoff[1], precision))
    elif not strict_labels:
        extra_statements.add(r'xticklabel={'
                               r'\pgfmathprintnumber['
                                 r'relative*={%i},relative style={std=%i:%i},'
                                 r'precision={%i}'
                               r']{\tick}'
                             r'}' % (exp_cutoff[0], exp_cutoff[0],
                                     exp_cutoff[1], precision))
        extra_statements.add(r'yticklabel={'
                               r'\pgfmathprintnumber['
                                 r'relative*={%i},relative style={std=%i:%i},'
                                 r'precision={%i}'
                               r']{\tick}'
                             r'}' % (exp_cutoff[0], exp_cutoff[0],
                                     exp_cutoff[1], precision))

    # Produce a pgfplot figure in a TeX file
    texpath = filename + '.tex'
    tikz_save(texpath, figure=figure, figurewidth='\\figurewidth',
              figureheight=None, textsize=textsize,
              tex_relative_path_to_data=tex_relative_path_to_data,
              strict=strict, draw_rectangles=draw_rectangles, wrap=wrap,
              show_info=show_info, extra=extra_statements)
    with open(texpath, 'r') as reader:
        src = reader.read()
    src = GROUP_RE.sub(GROUP_ADD,src)
    with open(texpath, 'w') as writer:
        writer.write(src)

    # Create a standalone PDF figure for immediate analysis
    if figure == 'gcf': 
        figure = mpl.pyplot.gcf()
    pdfpath = filename + '.pdf'
    figure.savefig(pdfpath)

