# Query Templates

```json title="study-config.json" linenums="56"
--8<-- "docs/study-config.example.json:56:65"
```

Query templates are defined through a list of substitutions.  Substitutions are
defined using two keys.  The `target` key is mandatory, containing the text
which is replaced in the query.  Targets must start with `{@` and end with
`@}`.  Target names are restricted to alphanumeric characters, and some
special characters like `-_:.`.  Then, either `replacement` or `file` are used,
with `replacement` providing the text directly, and `file` being the name of a
file under `boa/snippets/` which replaces `target`.  Care must
be taken to ensure that the query is valid Boa code after substitution is
completed.

Before performing substitutions, a substitutions list is constructed, first
from local substitutions then from global substitutions.  If two substitutions
define the same `target`, the first one defined is used.  Substitution will
iterate through the substitutions list until a loop has been completed without
any substitutions (i.e., a steady state has been reached).
