# coding: utf-8

from matplotlib import pyplot as plt
from typing import Dict, Any

__all__ = ["setup_plots"]

def setup_plots(rcParams: Dict[str, Any] = None):
    # avoid Type 3 fonts
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['ps.fonttype'] = 42

    plt.rcParams['figure.figsize'] = [6.0, 5.0]
    plt.rcParams['figure.dpi'] = 600.0
    plt.rcParams['font.size'] = 24
    if rcParams:
        for (k,v) in rcParams.items():
            plt.rcParams[k] = v

    plt.subplots(constrained_layout=True)
