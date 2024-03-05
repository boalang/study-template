Boa provides a Visual Studio Code extension on the [marketplace](https://marketplace.visualstudio.com/items?itemName=Boa.boalang) and the [Open VSX Registry](https://open-vsx.org/extension/Boa/boalang).

Note: While you can use this extension to write Boa queries, most functionality (like submitting/managing jobs) requires having a user/password on the Boa infrastructure. If you do not yet have one, please request a user.

## Features

### Editing Boa Queries
This extension provides support for writing Boa queries:

![Query Writing](https://github.com/boalang/vscode/raw/HEAD/images/syntax.gif)

This includes things like syntax highlighting, the ability to insert useful code snippets, code completion, and support for study template substitutions (templates).

### Submitting and Managing Boa Jobs
The extensions also provides support for submittin queries to Boa and managing existing jobs:

![Job Management](https://github.com/boalang/vscode/raw/HEAD/images/jobs.gif)

This allows you to effectively stay in the IDE and never need to go to the Boa website.

### Using Boa's Study Template
Boa provides a study template to help manage running empirical studies using Boa.

This plugin tightly integrates with the study template:

![Study Template](https://github.com/boalang/vscode/raw/HEAD/images/studytemplate.gif)

Providing support for managing the substitutions, running and downloading query output, and running analyses.

## Extension Settings

This extension contributes the following settings:

- `boalang.api.endpoint`: Boa API endpoint URL
- `boalang.login.username`: Boa API username
- `boalang.dataset.favorite`: Favorite Boa dataset
- `boalang.joblist.pagesize`: Number of jobs to show in the jobs tree view
- `boalang.output.size`: Size (in bytes) to limit displaying query outputs
- `boalang.joblist.autoload`: Should the jobs tree view refresh on extension activation?