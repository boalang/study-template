# coding: utf-8

from matplotlib import pyplot as plt

__all__ = ["setup_plots"]

def setup_plots(rcParams = None):
    plt.rcParams['figure.figsize'] = [6.0, 5.0]
    plt.rcParams['figure.dpi'] = 600.0
    plt.rcParams['font.size'] = 24
    if rcParams:
        for (k,v) in rcParams.items():
            plt.rcParams[k] = v
    plt.subplots(constrained_layout=True)
