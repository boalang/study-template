#!/usr/bin/env python3
# coding: utf-8

from common.df import get_df, get_deduped_df, get_decloned_df
from common.tables import get_styler, highlight_cols, highlight_rows, save_table

if __name__ == '__main__':
    names=['var', 'project', 'file', 'astcount']

    # get all of the data, remove no duplicates/clones
    df1 = get_df('rq1', 'kotlin', names=names)

    style = highlight_rows(highlight_cols(get_styler(df1['astcount'].describe())))
    save_table(style, 'rq1a.tex', 'kotlin')

    # remove any data where the ASTs were identical (keeping 1 copy of each cluster)
    df2 = get_deduped_df('rq1', 'kotlin', 'kotlin', names=names)

    style = highlight_rows(highlight_cols(get_styler(df2['astcount'].describe())))
    save_table(style, 'rq1b.tex', 'kotlin')

    # remove any data where the ASTs were *almost* identical (keeping 1 copy of each cluster)
    df3 = get_decloned_df('rq1', 'kotlin', 'kotlin', names=names)

    style = highlight_rows(highlight_cols(get_styler(df3['astcount'].describe())))
    save_table(style, 'rq1c.tex', 'kotlin')
