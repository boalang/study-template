#!/usr/bin/env python3
# coding: utf-8

from common.df import get_deduped_df
from common.tables import get_styler, highlight_cols, highlight_rows, save_table

if __name__ == '__main__':
    df = get_deduped_df('rq1', 'kotlin', names=['var', 'project', 'file', 'astcount'])
    df = df['astcount'].describe()

    style = highlight_rows(highlight_cols(get_styler(df)))
    save_table(style, 'rq1.tex', 'kotlin')
