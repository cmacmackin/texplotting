from matplotlib import rc
import matplotlib as mpl
import re

rc('text', usetex=True)
rc('font', **{'family':'serif', 'serif':[], 'sans-serif':[],
              'monospace':[]})
rc('pgf', texsystem='pdflatex')
rc('legend', **{'fontsize':'medium', 'frameon':False})

SCALEVAR = 'plotscale'
FONTVAR = 'plotfontsize'
PT_RE = re.compile(r'\\(pgfsetlinewidth|pgfsetdash\{\})\s*\{\s*([0-9.]+)\s*pt\s*\}')
FONT_RE = re.compile(r'\\fontsize\s*\{\s*([0-9.]+)\s*\}\s*\{\s*([0-9.]+)\s*\}')
PT_SUB = r'\pgfmathparse{{\2/\{}}}\\\1{{\pgfmathresult pt}}'.format(SCALEVAR)
FONT_SUB = r'\\fontsize{{\{0}}}{{1.2\{0}}}'.format(FONTVAR)
FONTSET = r'''
\makeatletter
\pgfmathparse{{\f@size/\{1}}}
%\FPdiv\{0}num\f@size\{1}
\makeatother
\ifcsname {0}\endcsname\else
\newlength\{0}
\fi
\setlength{{\{0}}}{{\pgfmathresult pt}}
'''.format(FONTVAR,SCALEVAR)


def savetex(filename, figure='gcf'):
    '''
    Provides a wrapper for saving matplotlib figures in the pgf
    format, but with certain modificatiosn to make them easy to scale.
    The plot can then be included in a LaTeX file as follows:
    
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
    :returns: None
    
    '''
    if figure == 'gcf': 
        figure = mpl.pyplot.gcf()
    
    # Produce a pgfplot figure in a TeX file
    texpath = filename + '.pgf'
    figure.savefig(texpath)
    pgf = FONTSET
    with open(texpath,'r') as reader:
        pgf += reader.read()
    pgf = PT_RE.sub(PT_SUB,pgf)
    pgf = FONT_RE.sub(FONT_SUB,pgf)
    with open(texpath,'w') as writer:
        writer.write(pgf) 

    # Create a standalone PDF figure for immediate analysis
    pdfpath = filename + '.pdf'
    figure.savefig(pdfpath)

