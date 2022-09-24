# coding: utf-8

import os
import pandas as pd
import sys
from typing import Optional

from .utils import _resolve_dir, _get_dir

__all__ = [
    "get_styler",
    "highlight_cols",
    "highlight_rows",
    "save_table",
    ]

def get_styler(df: pd.DataFrame|pd.Series) -> pd.io.formats.style.Styler:
    if isinstance(df, pd.Series):
        return df.to_frame().style
    return df.style

def highlight_cols(styler: pd.io.formats.style.Styler) -> pd.io.formats.style.Styler:
    styler = styler.applymap_index(lambda x: 'textbf:--rwrap;', axis='columns')
    return styler.hide(names=True, axis='columns')

def highlight_rows(styler: pd.io.formats.style.Styler) -> pd.io.formats.style.Styler:
    styler = styler.applymap_index(lambda x: 'textbf:--rwrap;', axis='index')
    return styler.hide(names=True, axis='index')

_colsepname = ''
def save_table(styler: pd.io.formats.style.Styler, filename: str, subdir: Optional[str]=None, decimals: Optional[int]=2, thousands: Optional[str]=',', colsep: Optional[str]=None, **kwargs):
    '''Saves a DataFrame to a LaTeX table.

    Args:
        styler (pd.io.formats.style.Styler): A Pandas Styler object for formatting a table.
        filename (str): The filename to save to, including '.tex' extension. Files are saved under 'tables/'.
        subdir (Optional[str]): the sub-directory, underneath 'tables/', to save in. Defaults to None.
        decimals (Optional[int]): How many decimal places for floats. Defaults to 2.
        thousands (Optional[str]): What mark should be used for thousands separator.  Defaults to ','.
        colsep (Optional[str]): If False, use default column separators.  If a string, it is the column separator units. Defaults to False.
    '''
    global _colsepname
    if colsep:
        _colsepname = _colsepname + 'A'

    with pd.option_context("max_colwidth", 1000):
        styler = styler.format_index(None, escape='latex', axis='columns')
        styler = styler.format_index(None, escape='latex', axis='index')
        tab1 = styler.format(None, precision=decimals, thousands=thousands, escape='latex').to_latex(**kwargs)

    os.makedirs(_resolve_dir(f'tables/{_get_dir(subdir)}'), 0o755, True)
    with open(_resolve_dir(f'tables/{_get_dir(subdir)}{filename}'), 'w', encoding='utf-8') as f:
        f.write('% DO NOT EDIT\n')
        f.write('% this file was automatically generated by ' + os.path.basename(sys.argv[0]) + '\n')
        if colsep:
            f.write('\\newcommand{\\oldtabcolsep' + _colsepname + '}{\\tabcolsep}\n')
            f.write('\\renewcommand{\\tabcolsep}{' + colsep + '}\n')
        f.write(tab1)
        if colsep:
            f.write('\\renewcommand{\\tabcolsep}{\\oldtabcolsep' + _colsepname + '}\n')
