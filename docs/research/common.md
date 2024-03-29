# Using the Common Library

The study template provides a common Python library to help researchers generate tables and figures from their analyses.


## Data Management

The `common.df` library provides two functions for reading Boa output into a Pandas dataframe, these are `get_df` and `get_deduped_df`.  These functions take similar basic arguments.  These functions will read from a Parquet file if it has been generated, otherwise, they will read from CSV (and save to parquet for sped-up loading later on).  Basic call syntax is below, with description of arguments following.


```python title="Helpers for reading Boa output into Pandas dataframes"
# read all data
get_df(filename: str, subdir: Optional[str]=None,
       drop: Optional[List[str]]=None,
       precache_function: Optional[Callable[[pd.DataFrame], pd.DataFrame]]=None,
       **kwargs) -> pd.DataFrame

# read de-duplicated data
get_deduped_df(filename: str, subdir: Optional[str]=None, dupesdir: Optional[str]=None,
               drop: Optional[List[str]]=None,
               precache_function: Optional[Callable[[pd.DataFrame], pd.DataFrame]]=None,
               ts: bool=False, **kwargs) -> pd.DataFrame
```

 - `filename`: the name of the CSV data file, without `.csv`.
 - `subdir`: optional, the name of the sub-directory underneath `data/csv/` that `filename` is in (default `None`).
 - `dupesdir`: (`get_deduped_df` only): optional, the name of the sub-directory underneath `data/csv` containing the dupes file (default `None`).
 - `drop`: A list of column names to drop after loading.
 - `precache_function`: A function that takes a data frame, and transforms it in some way (e.g., creating new columns which are intensive to compute, or converting data types).
 - `ts` (`get_deduped_df` only): Pass `True` if the hash file also has file timestamps.
 - `**kwargs`: When reading from CSV, these are passed to [`pd.read_csv`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html).
 
An example of the usage of `get_deduped_df` is shown below.

```python title="analyses/rq1.py" linenums="8"
    df = get_deduped_df('rq1', 'kotlin', 'kotlin', names=['var', 'project', 'file', 'astcount'])
```

This will get a file-wise deduplicated dataframe from the results file `rq1.csv` in `data/csv/kotlin/`, using the `data/csv/kotlin/dupes.csv` file to provide duplication information.  It gives the columns the names `var`, `project`, `file`, and `astcount`.

### Deduplication

Since data duplication is a known problem in MSR studies (see [Lopes et al., 2017](https://dl.acm.org/doi/10.1145/3133908)), we provide the ability to deduplicate data.  However, this deduplication is based on AST hashes.  This is done by calculating the hash of the AST of each file as it appears in the HEAD commit of each repository, and selecting one project/file pair for each hash value.  A query for this is provided, see also [Defining Queries](add-query.md#defining-queries).

## Table Generation

Pandas can be used to generate LaTeX tables from query output and calculated data, however, much of this is routine and enabled by `common.tables`.  In particular, `common.tables` generates tables that use the [`booktabs`](https://ctan.org/pkg/booktabs/) package for formatting (following the ACM document class recommendations).

To do this, there are four major functions:

 - `get_styler` which returns a [`Styler`](https://pandas.pydata.org/pandas-docs/stable/reference/style.html) object for a dataframe or series.  Stylers are used to format data based on the values of each cell.  In addition to the dataframe or series, it takes two keyword arguments: a number of `decimals` (default 2), and a `thousands` separator (default `,`).
 - `highlight_cols` and `highlight_rows`: These highlight the column and row headers, respectively of a table in a `Styler` object, as shown below on line 11.
 - `save_table` will save a `Styler` to a LaTeX table.  Its usage is somewhat more complex, and is described below.
 
```python title="analyses/rq1.py" linenums="11"
    style = highlight_rows(highlight_cols(get_styler(df)))
    save_table(style, 'rq1.tex', 'kotlin')
```

### Using `save_table`

```python title="The save_table() function"
def save_table(styler: pandas.io.formats.style.Styler, filename: str,
               subdir: Optional[str]=None,
               mids: Optional[Union[RuleSpecifier, List[RuleSpecifier]]]=None,
               colsep: Optional[str]=None, **kwargs):
```

`save_table` takes two mandatory arguments, a `styler`, and a `filename` (which should include the `.tex` extension).  It takes an optional `subdir` (underneath `tables/`) to save the file in as well.  Additionally, the keyword argument `colsep` is available to use a custom column separator width, if no argument (or `None`) is passed, defaults will be used, otherwise, the value should be the size of the column separator in LaTeX compatible units.

Additionally, a `mids` keyword argument is available to allow manual placement of mid-table rules.  If `None`, no mid-table rules will be passed, otherwise, a rule specifier or a list of rule specifiers may be passed, as described below.

`RuleSpecifier`s take the following form:

 - A single integer $n$, which will place a `\midrule` after the $n$th line (one-based indexing).
 - A pair `(n, width)` will place `\midrule[width]` after the $n$th line.
 - A pair `(n, cmidrulespec)` or `(n, [cmidrulespec+])`, which will place the specified `cmidrules` after the $n$th line.  A `cmidrulespec` is a tuple, `(start, end, left_trim, right_trim)`, where `start` and `end` are column indices, and `left_trim` and `right_trim` are either Booleans or LaTeX lengths.  If they are False, no trim will be applied, if they are True, default trim will be applied, if they are a LaTeX length, a trim of that length will be applied.

Finally, additional keyword arguments may be passed to [`styler.to_latex`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.io.formats.style.Styler.to_latex.html), to further control generated appearance.  Options of note include `multirow_align` to control the vertical alignment of row-spanning cells, `multicol_align` to control the horizontal alignment of column-spanning cells, and `siunitx` to enable [`siunitx`](https://ctan.org/pkg/siunitx)-style numerical alignment.

## Figure Generation

The `df.graphs` module provides a function, `setup_plots` to create a blank, pre-configured plot canvas for use.  It takes an optional argument, `rcParams`, which is used to set the [`plt.rcParams`](https://matplotlib.org/stable/users/explain/customizing.html) parameters.  In particular, the following are set by default:

 - PDF and PS font types are set to 42, avoiding PostScript Type 3 fonts (for compliance with common submission requirements).
 - Figure size is set to 6"x4", with 600 DPI.
 - Font size is set to 24 pt.
 - Plots are set in a constrained layout (see [Matplotlib's constrained layout guide](https://matplotlib.org/stable/users/explain/axes/constrainedlayout_guide.html) for more information).

## Utilities

Finally, a few utilities are provided in `common.utils`.  These are mostly intended for helping to simplify analyses, and are as follows:

 - `get_dataset` will take a filename base name and optional sub-directory name, and determine which Boa dataset the data came from.

## Loading Common Libraries

The common libraries described above can be loaded as normal in most cases.  However, if analyses are arranged in various subdirectories, the following code can be used to allow import.

```python title="Code to import common from a subdirectory of 'analyses/'."
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent)) # (additional calls to parent may be necessary for deeply-nested analyses)
```
