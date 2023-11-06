# coding: utf-8

import os
import pandas as pd
import pandas.io.formats.style
import re
import sys
from typing import List, Optional, Union, Tuple

from .utils import _resolve_dir, _get_dir

__all__ = [
    "get_styler",
    "highlight_cols",
    "highlight_rows",
    "save_table",
    ]
def get_styler(df: Union[pd.DataFrame, pd.Series], decimals: Optional[int]=2, thousands: Optional[str]=',') -> pandas.io.formats.style.Styler:
    '''Gets a Styler object for formatting a table.
    
    Args:
        decimals (Optional[int]): How many decimal places for floats. Defaults to 2.
        thousands (Optional[str]): What mark should be used for thousands separator.  Defaults to ','.
    '''
    if isinstance(df, pd.Series):
        styler = df.to_frame().style
    else:
        styler = df.style
    return styler.format(None, precision=decimals, thousands=thousands, escape='latex')

def highlight_cols(styler: pandas.io.formats.style.Styler) -> pandas.io.formats.style.Styler:
    styler = styler.applymap_index(lambda x: 'textbf:--rwrap;', axis='columns')
    return styler.hide(names=True, axis='columns')

def highlight_rows(styler: pandas.io.formats.style.Styler) -> pandas.io.formats.style.Styler:
    styler = styler.applymap_index(lambda x: 'textbf:--rwrap;', axis='index')
    return styler.hide(names=True, axis='index')

def _trim_spec(trim_left, trim_right):
    if trim_left or trim_right:
        trim_spec = '('
        if trim_left:
            trim_spec += 'l'
            if isinstance(trim_left, str):
                trim_spec += f"{{{trim_left}}}"
        if trim_right:
            trim_spec += 'r'
            if isinstance(trim_right, str):
                trim_spec += f"{{{trim_right}}}"
        trim_spec += ')'
        return trim_spec
    else:
        return ''

def rule_from_spec(spec: rule_specifier) -> Tuple[int, str]:
    match spec:
        case int(row):
            return (row, '\midrule')
        case (int(row), str(width)):
            return (row, f'\\midrule[{width}]')
        case (int(row), list(specs)) | (int(row), specs):
            specs = specs if isinstance(specs, list) else [specs]
            specs = sorted(specs, key=lambda x: x[0])
            rules = []
            for spec in specs:
                rules.append(f'\\cmidrule{_trim_spec(spec[2], spec[3])}{{{spec[0]}-{spec[1]}}}')
            return (row, ' '.join(rules))
        case _:
            return (-1, "Unhandled case")

def save_table(styler: pandas.io.formats.style.Styler, filename: str, subdir: Optional[str]=None,
               mids: Optional[Union[int,
                                    Tuple[int, str],
                                    Tuple[int, Union[List[int, int, Union[bool, str], Union[bool, str]]]],
                                    List[Union[int,
                                               Tuple[int, str],
                                               Tuple[int, Union[List[int, int, Union[bool, str], Union[bool, str]]]]]]]]=None,
               colsep: Optional[str]=None, **kwargs):
    '''Saves a DataFrame to a LaTeX table.

    Args:
        styler (pandas.io.formats.style.Styler): A Pandas Styler object for formatting a table.
        filename (str): The filename to save to, including '.tex' extension. Files are saved under 'tables/'.
        subdir (Optional[str]): the sub-directory, underneath 'tables/', to save in. Defaults to None.
        mids (Optional[Union[x=Union[int,
                                     Tuple[int, str],
                                     Tuple[int, Union[List[int, int, Union[bool, str], Union[bool, str]]]]],
                             List[x]]]): Specification of mid-table rules, as follows:
           - row : place a \midrule after this row
           - (row, width) : place a midrule with a width of str after row
           - (row, [(left, right, trimleft, trimright)]) : place a series of \cmidrule(trimleft,trimright){left-right} afer row
        colsep (Optional[str]): If False, use default column separators.  If a string, it is the column separator units. Defaults to False.
    '''
    if colsep:
        colsepprefix = re.sub('[0-9]', '',
                              filename.split('.')[0] \
                                      .replace(' ', '') \
                                      .replace('_', ''))

    with pd.option_context("max_colwidth", 1000):
        styler = styler.format_index(None, escape='latex', axis='columns')
        styler = styler.format_index(None, escape='latex', axis='index')
        styler = styler.set_table_styles([
                {'selector': 'toprule', 'props': ':toprule;'},
                {'selector': 'bottomrule', 'props': ':bottomrule;'},
            ], overwrite=False)
        tab1 = styler.to_latex(**kwargs)

    if mids is not None:
        if not isinstance(mids, list):
            mids = [mids]
        rules = sorted([rule_from_spec(mid) for mid in mids], key=lambda x: x[0])
        lines = tab1.splitlines()
        offset = 0
        for line, rule in rules:
            lines.insert(offset + line + 2, rule)
            offset += 1
        tab1 = '\n'.join(lines)

    os.makedirs(_resolve_dir(f'tables/{_get_dir(subdir)}'), 0o755, True)
    with open(_resolve_dir(f'tables/{_get_dir(subdir)}{filename}'), 'w', encoding='utf-8') as f:
        f.write('% DO NOT EDIT\n')
        f.write('% this file was automatically generated by ' + os.path.basename(sys.argv[0]) + '\n')
        if colsep:
            f.write('\\newcommand{\\oldtabcolsep' + colsepprefix + '}{\\tabcolsep}\n')
            f.write('\\renewcommand{\\tabcolsep}{' + colsep + '}\n')
        f.write(tab1)
        if colsep:
            f.write('\\renewcommand{\\tabcolsep}{\\oldtabcolsep' + colsepprefix + '}\n')
