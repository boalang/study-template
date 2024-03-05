Boa provides a Visual Studio Code extension on the [marketplace](https://marketplace.visualstudio.com/items?itemName=Boa.boalang) and the [Open VSX Registry](https://open-vsx.org/extension/Boa/boalang).

/// admonition | Boa API Access
    type: warning

While you can use this extension to view and write Boa queries, most functionality (like submitting and managing jobs) requires having a user/password on the Boa infrastructure. If you do not yet have one, please [request a user](https://boa.cs.iastate.edu/request/).
///

## Features

### Viewing and Writing Boa Queries

This extension provides support for viewing and writing Boa queries:

![Query Writing](https://github.com/boalang/vscode/raw/HEAD/images/syntax.gif)

This includes things like syntax highlighting, the ability to insert useful code snippets, code completion, and support for study template substitutions (templates).

Any substitutions in the `study-config.json` are automatically highlighted by the editor.  If you hover over one, you can see the value it will be replaced with.  The code completion also includes these substitutions.

Note that since the editor does not know the context of which query you are editing, it will show all possible substitutions that could match.  If you want to view the file for a particular query, you can click the preview button in the top right of the editor and select the query you want to preview it for.

### Submitting and Managing Boa Jobs

The extensions also provides support for submitting queries to Boa and managing existing jobs:

![Job Management](https://github.com/boalang/vscode/raw/HEAD/images/jobs.gif)

This allows you to effectively stay in the IDE and never need to go to the Boa website.

### Using Boa's Study Template

If you are using the study template, either for a new study or a replication package, the extension provides additional support for managing the study:

![Study Template](https://github.com/boalang/vscode/raw/HEAD/images/studytemplate.gif)

Simply open the `study-config.json` file and you will see several code actions available to you that allow you to download specific outputs, clean data, run specific analyses, etc.  This is an alternative to running `make` on the command line.  There is also a tree view that shows the various outputs and analyses that can be run and allows clicking on it to run them.

Most of the filenames shown in the file can also be clicked on to open the file in the editor.

## Extension Settings

The extension will automatically prompt you for your Boa API credentials the first time you use it.

This extension also contributes the following settings:

- `boalang.dataset.favorite`: Favorite Boa dataset
- `boalang.joblist.pagesize`: Number of jobs to show in the jobs tree view
- `boalang.output.size`: Size (in bytes) to limit displaying query outputs
- `boalang.joblist.autoload`: Should the jobs tree view refresh on extension activation?
