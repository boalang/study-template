# Using the Common Library

The study template provides a common Python library to help researchers generate tables and figures from their analyses.


## Data Management

The `common.df` library provides two functions for reading Boa output into a Pandas dataframe, these are `get_df` and `get_deduped_df`.  These functions take similar basic arguments.  These functions will read from a Parquet file if it has been generated, otherwise, they will read from CSV (and save to parquet for sped-up loading later on).  Basic call syntax is below, with description of arguments following.


```python title="Call Syntax"
get_df(filename: str, subdir: Optional[str]=None, drop: Optional[List[str]]=None,
       precache_function: Optional[Callable[[pd.DataFrame], pd.DataFrame]]=None,
       **kwargs) -> pd.DataFrame
       
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
 - `**kwargs`: When reading from CSV, these are passed to [`pd.read_csv`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html), which see.
 
An example of the usage of `get_deduped_df` is shown below.

```python title="analyses/rq1.py" linenums="8"
--8<-- "docs/research/rq1.py:8:8"
```

This will get a file-wise deduplicated dataframe from the results file `rq1.csv` in `data/csv/kotlin/`, using the `data/csv/kotlin/dupes.csv` file to provide duplication information, with the columns given the names `var`, `project`, `file`, and `astcount`.

### Deduplication

TODO

## Table Generation

## Figure Generation

## Utilities

## Loading Common Libraries

The common libraries described above can be loaded as normal in most cases.  However, if analyses are arranged in various subdirectories, the following code can be used to allow import.

```python
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent)) # (additional calls to parent may be necessary for deeply-nested analyses)
```
