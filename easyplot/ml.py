import numpy as np
import matplotlib.pyplot as plt


class METRIC:
    def __init__(self, y_pred, y_true):
        self.y_pred = y_pred
        self.y_true = y_true

    def __call__(self):
        print("MAE:", self.mae())
        print("RMSE:", self.rmse())
        print("R2:", self.r2_score())

    def mae(self):
        return np.absolute(self.y_pred - self.y_true).mean()

    def rmse(self):
        return np.sqrt(((self.y_pred - self.y_true)**2).mean())

    def r2_score(self):
        ssr = ((self.y_pred - self.y_true)**2).sum()
        y_mean = self.y_true.mean()
        sst = ((self.y_true - y_mean)**2).sum()
        return 1 - ssr/sst


def parityplot(plots, dft, nn, labels, colors, tag,
               marker='o', markersize=1, savefig=False, figname=None):
    """Plot parity plot for DFT and NN predictions.

    Args:
        plots (EasyPlot): EasyPlot object.
        dft (dict): DFT results of energies and forces, the keys are 
                    [sys]['idx']['E'] or [sys]['idx']['F'].
        nn (dict): NN results of energies and forces, the keys are 
                    [sys]['idx']['pred_E'] or [sys]['idx']['pred_F'].
        label (list): labels for each system.
        color (list): colors for each system.
        markersize (int): marker size.
        marker (str): marker style.
        savefig (bool): save figure or not.

        """

    pe, pf = plots()
    critical_E, critical_F = [], []

    # scatter plot
    for idx, s in enumerate(dft.keys()):
        dft_E, dft_F = [], []
        for i in dft[s].keys():
            dft_E.append(dft[s][i]['E'])
            dft_F.append(dft[s][i]['F'].flatten())
        dft_E = np.array(dft_E)
        dft_F = np.concatenate(dft_F)
        critical_E += [dft_E.min(), dft_E.max()]
        critical_F += [dft_F.min(), dft_F.max()]

        nn_E, nn_F = [], []
        for i in nn[s].keys():
            nn_E.append(nn[s][i]['pred_E'])
            nn_F.append(nn[s][i]['pred_F'].flatten())
        nn_E = np.array(nn_E)
        nn_F = np.concatenate(nn_F)

        print(f'[{s}] Energies metrics:')
        METRIC(nn_E, dft_E)()
        print(f'[{s}] Forces metrics:')
        METRIC(nn_F, dft_F)()
        print('')

        pe.scatterplot(dft_E, nn_E, label=labels[idx], markersize=markersize,
                       marker=marker, color=colors[idx])
        pf.scatterplot(dft_F, nn_F, label=labels[idx], markersize=markersize,
                       marker=marker, color=colors[idx])

    pe.set_labels(xlabel='DFT_E (eV/atom)', ylabel='NN_E (eV/atom)')
    pf.set_labels(xlabel='DFT_F (eV/$\AA$)', ylabel='NN_F (eV/$\AA$)')

    pe.set_legend(markerscale=6)
    pf.set_legend(markerscale=6)

    pe.set_subtitle(f'{tag} Energies')
    pf.set_subtitle(f'{tag} Forces')

    # parity line
    critical_E = [min(critical_E), max(critical_E)]
    critical_F = [min(critical_F), max(critical_F)]
    pe.lineplot(critical_E, critical_E,
                color='black', linestyle='--', linewidth=1)

    pf.lineplot(critical_F, critical_F,
                color='black', linestyle='--', linewidth=1)

    plt.tight_layout()
    if savefig:
        plots.save(f"images/{figname}.pdf")
