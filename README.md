# sawmill

Simple, beautiful, powerful data analysis and reporting for your logs.

## Setup

### Users

1. Install pipx
2. Use pipx to install `sawmill`
```sh
pipx install sawmill
```
3. The user is ready to call `sawmill` from the command line!

4. See [Usage](#usage)

### Developers

1. Install the [pnpm package manager](https://pnpm.io/installation)
2. The development environment assumes [Visual Studio Code](https://code.visualstudio.com/download) as the default project code editor, with the following plugins:
    - Required: 
        - [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid)
    - Recommended: 
        - [Mermaid Chart](https://marketplace.visualstudio.com/items?itemName=MermaidChart.vscode-mermaid-chart) (free to sign up for an account?)
3. Clone the repository
```sh
# if the user has ssh access to GitHub
git clone git@github.com:bengineerdavis/sawmill.git
```

for everyone else ...

```sh
git clone https://github.com/bengineerdavis/sawmill.git
```
4. Install [`pipx`](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)
5. Use `pipx` to install `poetry`
```sh
pipx install poetry
```
6. OPTIONAL: the user may set up their own `virtual environment` or let `poetry` to manage it for them
7. Navigate into the new local `sawmill` directory
```sh
cd sawmill
```
8. Use pipx to make an editable installation of sawmill on the user's local machine
```sh
pipx install -e .
```
9. Install project dependencies 
```sh
make install
``` 
10. Ready to contribute!

## Usage

```bash
# command returns pandas DataFrame with user-select columns and rows defined in the SQL script

sawmill [path/to/file] [sql command string]|[sql command from file.sql]

