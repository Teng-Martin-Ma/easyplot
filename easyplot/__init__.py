import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib_inline import backend_inline
import matplotlib as mpl
mpl.rcParams["figure.autolayout"] = True
mpl.rcParams['pdf.fonttype'] = 42  # true-type for adobe editor
mpl.rcParams['pdf.compression'] = 0  # 0-9, 0 disable compression
backend_inline.set_matplotlib_formats('retina')
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.dpi'] = 300


cmap = ['#0F4CB1',  # 2020 Classic Blue
        '#BF1932',  # 2002 True Red
        '#88B04B',  # 2017 Greenery
        '#F5DF4D',  # 2021 Illuminating
        '#009473',  # 2013 Emerald
        ]


line_styles = ['-', '--', '-.', ':']
marker_styles = ['o', '.', '^', 's', 'p', '*', 'P']


class EasyPlot:
    """
    Args:
        nrows (int): number of rows
        ncols (int): number of columns
        figsize (tuple): figure size

    """

    def __init__(self, nrows, ncols, figsize=None, **kwargs):
        if figsize is None:
            figsize = (ncols * 6, nrows * 4)
        self.fig, axes = plt.subplots(nrows, ncols, figsize=figsize, **kwargs)
        if nrows == 1 and ncols == 1:
            self.axes = [axes]
        else:
            self.axes = axes.flatten()

    def __call__(self):
        return [Main(ax) for ax in self.axes]

    def save(self, filename):
        self.fig.savefig(filename)


class Main(EasyPlot):
    """
    Args:
        ax (matplotlib.axes._subplots.AxesSubplot): axes
    """

    def __init__(self, ax):
        self.ax = ax

    def lineplot(self, x, y, label=None, linewidth=1, linestyle=None,
                 color=None, dotcolor=None, with_dots=False, minor_ticks=True):
        ax = self.ax
        ax.plot(x, y, label=label, lw=linewidth,
                color=color, ls=linestyle)
        if with_dots:
            ax.scatter(x, y, s=10, color=dotcolor)
        if minor_ticks:
            ax.xaxis.set_minor_locator(AutoMinorLocator(5))
            ax.yaxis.set_minor_locator(AutoMinorLocator(5))
        ax.grid(ls='--', lw=0.5, alpha=1)

    def scatterplot(self, x, y, label=None, color=None, marker=None,
                    markersize=10, minor_ticks=True):
        ax = self.ax
        ax.scatter(x, y, label=label, s=markersize,
                   c=color, marker=marker)
        if minor_ticks:
            ax.xaxis.set_minor_locator(AutoMinorLocator(5))
            ax.yaxis.set_minor_locator(AutoMinorLocator(5))
        ax.grid(ls='--', lw=0.5, alpha=1)

    def barplot(self, x, h, width=0.5, color=None):
        ax = self.ax
        ax.bar(x, h, width=width,
               color=cmap[self.count] if color is None else color,)
        ax.grid(ls='--', lw=0.5, alpha=1)

    def bbarplot(self, x, h1, h2, width=0.3, hlabels=None):
        ax = self.ax
        ax.bar(x - width/2, h1, width=width, color=cmap[0], label=hlabels[0])
        ax.bar(x + width/2, h2, width=width, color=cmap[1], label=hlabels[1])
        ax.grid(ls='--', lw=0.5, alpha=1)

    def histplot(self, x, bins=100, color=None, norm=False):
        ax = self.ax
        ax.hist(x, bins=bins, density=norm,
                color=cmap[self.count] if color is None else color,)

    def set_legend(self, loc=None, markerscale=1):
        ax = self.ax
        if loc is None:
            ax.legend(loc='best', markerscale=markerscale)
        else:
            ax.legend(bbox_to_anchor=loc, markerscale=markerscale)

    def set_labels(self, xlabel=None, ylabel=None, fontsize=12):
        ax = self.ax
        ax.set_xlabel(xlabel, fontsize=fontsize)
        ax.set_ylabel(ylabel, fontsize=fontsize)

    def set_subtitle(self, subtitle, loc='left'):
        ax = self.ax
        ax.set_title(subtitle, loc=loc)

    def set_tickstyle(self, x=True, y=False, ts='sci',):
        '''tick style (str): sci, plain'''
        ax = self.ax
        if x:
            ax.ticklabel_format(axis='x', style=ts, scilimits=(0, 0))
        if y:
            ax.ticklabel_format(axis='y', style=ts, scilimits=(0, 0))

    def set_ticklabel(self, x=None, xticklabel=None, y=None,
                      yticklabel=None, fontsize=12):
        ax = self.ax
        if x is not None:
            ax.set_xticks(x, xticklabel, fontsize=fontsize)
        if y is not None:
            ax.set_yticks(y, yticklabel, fontsize=fontsize)

    def set_limit(self, xlim=None, ylim=None):
        ax = self.ax
        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)

    def set_fill(self, x, y1, y2=0, color=cmap[-1], alpha=0.2):
        ax = self.ax
        ax.fill_between(x, y1, y2, color=color, alpha=alpha)
