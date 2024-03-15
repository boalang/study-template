# Using the Common Library

The study template provides a common Python library to help researchers generate tables and figures from their analyses.


## Data Management

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
