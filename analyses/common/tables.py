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
    "auto_header_rules",
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

RuleLineIndex = int
RuleWidth = str
TrimSpec = Union[bool, RuleWidth]
CmidruleSpec = Tuple[int, int, TrimSpec, TrimSpec]
RuleSpecifier = Union[RuleLineIndex,
                       Tuple[RuleLineIndex, RuleWidth],
                       Tuple[RuleLineIndex, Union[CmidruleSpec, List[CmidruleSpec]]]]
ConcreteRule = Tuple[RuleLineIndex, str]

def _trim_spec(trim_left: TrimSpec, trim_right: TrimSpec) -> str:
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

def _rule_from_spec(spec: RuleSpecifier) -> ConcreteRule:
    match spec:
        case RuleLineIndex(row):
            return (row, '\midrule')
        case (RuleLineIndex(row), RuleWidth(width)):
            return (row, f'\\midrule[{width}]')
        case (RuleLineIndex(row), list(specs)) | (RuleLineIndex(row), specs):
            specs = specs if isinstance(specs, list) else [specs]
            specs = sorted(specs, key=lambda x: x[0])
            rules = []
            for spec in specs:
                rules.append(f'\\cmidrule{_trim_spec(spec[2], spec[3])}{{{spec[0]}-{spec[1]}}}')
            return (row, ' '.join(rules))
        case _:
            print(f"Rule {spec!r} is invalid.", file=sys.err)
            return (-1, "Unhandled case")

def auto_header_rules(df: pd.DataFrame, skip_index: bool=True, level: int=0, left_trim: TrimSpec=True, right_trim: TrimSpec=True) -> List[RuleSpecifier]:
    index_cols = 1
    if isinstance(df.index, pd.MultiIndex):
        index_cols = df.index.nlevels
    if not isinstance(df.columns, pd.MultiIndex):
        if skip_index:
            return [(1, (1 + index_cols, df.columns.size + index_cols, False, False))]
        else:
            return [1]
    else:
        if not skip_index:
            return [df.columns.nlevels]
        values = df.columns.get_level_values(level).array
        starts = []
        cur = values[0]
        cur_start = 1
        val = 1
        for label in values[1:]:
            if label != cur:
                cur = label
                if cur_start == 1:
                    starts.append((cur_start + index_cols, val + index_cols, False, right_trim))
                else:
                    starts.append((cur_start + index_cols, val + index_cols, left_trim, right_trim))
                cur_start = val + 1
            val += 1
        starts.append((cur_start + index_cols, len(values) + index_cols, left_trim, False))
        return [(df.columns.nlevels, starts)]

def save_table(styler: pandas.io.formats.style.Styler, filename: str, subdir: Optional[str]=None,
               mids: Optional[Union[RuleSpecifier, List[RuleSpecifier]]]=None,
               colsep: Optional[str]=None, **kwargs):
    '''Saves a DataFrame to a LaTeX table.

    Args:
        styler (pandas.io.formats.style.Styler): A Pandas Styler object for formatting a table.
        filename (str): The filename to save to, including '.tex' extension. Files are saved under 'tables/'.
        subdir (Optional[str]): the sub-directory, underneath 'tables/', to save in. Defaults to None.
        mids (Optional[Union[RuleSpecifier, List[RuleSpecifier]]]): Specification of mid-table rules, where a RuleSpecifier is one of the following:
           - RuleLineIndex (an int): place a \midrule after the specified row.
           - Tuple[RuleLineIndex, RuleWidth]: Place a \midrule[RuleWidth] after the specified row.
           - Tuple[RuleLineIndex, Union[CmidruleSpec, List[CmidruleSpec]]] where, CmidruleSpec is Tuple[lstart: int, rstart: int, ltrim: TrimSpec, rtrim: TrimSpec] and TrimSpec is Union[bool, RuleWidth]:
             Place a (series of) \cmidrule(ltrim rtrim){lstart-rstart} after the specified row. ltrim is 'l' if true, 'l{width}' if a RuleWidth, similarly for rtrim.
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
        rules = filter(lambda x: x[0] >= 0, sorted([_rule_from_spec(mid) for mid in mids], key=lambda x: x[0]))
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
