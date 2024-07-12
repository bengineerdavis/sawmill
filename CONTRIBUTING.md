# Contributing to Sawmill

Thank you for your interest in contributing to Sawmill! This document provides
guidelines for making contributions to the project. By participating in this project,
you agree to abide by its terms.

## Table of Contents

* [Prerequisites](#prerequisites)
* [Getting Started](#getting-started)
* [Issues](#issues)
    * [Reporting Issues](#reporting-issues)
* [Pull Requests](#pull-requests)
    * [Branching](#branching)
    * [Commits](#commits)
    * [Pull Requests](#pull-requests)
* [Code Review](#code-review)
* [Project Tools](#project-tools)


## Prerequisites

This project expects the following from contributors:

- They should review and understand the entirety of the project's [README](./README.md):
- The contributor must already meet the project's [user
  requirements](./README.md#user-requirements)
- be reasonably comfortable writing and reading **Python**  and **SQL** code
- an advanced-beginner-to-intermediate knowledge of the topics in the [Recommended
  Learning Resources](./docs/recommended-learning-resources.md) file
- a GitHub account
- a familiarity with the structure of the project's codebase

[Back to Table of Contents](#table-of-contents)

## Project Tools

Please have these tools installed and ready to use on your local machine before
contributing to the project:

- [pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation), which the
  project uses for python version and python venv dependency management
    - **Important**: review and complete the 
    [pyenv build environment instructions](https://github.com/pyenv/pyenv/wiki#suggested-build-environment) 
     (for your preferred installation method) before installing pyenv
- [pnpm](https://pnpm.io/installation), which the project uses for managing Node.js dependencies for Mermaid.js-generated charts and graphs
- [Makefiles](https://www.gnu.org/software/make/), which the project uses for automating
  tasks
- [pipx](https://pipx.pypa.io/stable/installation/) for installing sawmill for local
  user/QA testing
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) for version
  control
- [Visual Studio Code](https://code.visualstudio.com/download) with these plugins:
    - Required: [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid)
    - Recommended: [Mermaid
      Chart](https://marketplace.visualstudio.com/items?itemName=MermaidChart.vscode-mermaid-chart)
- [Poetry](https://python-poetry.org/docs/#installing-with-pipx), for managing Python
  dependencies, _install with pipx by following the steps in the Poetry link_

## Getting Started

Before you begin:
- Ensure you have Python 3.12, or higher, installed. If not, install it from the 
[Python website](https://www.python.org/downloads/).

- Set up the project on your local machine. Here’s how:

1. Make sure all [Project Tools](#project-tools) are installed and ready to go on your
   local machine.
2. Clone the repository:
    ```sh
    git clone git@github.com:bengineerdavis/sawmill.git
    ```
    Or:
    ```sh
    git clone https://github.com/bengineerdavis/sawmill.git
    ```
3. Navigate to the Sawmill directory:
    ```sh
    cd sawmill
    ```
4. Install Sawmill locally in editable mode:
    ```sh
    pipx install -e .
    ```

6. Set up a virtual environment first, or let [Poetry manage it](https://python-poetry.org/docs/managing-environments/).
7. Install project dependencies:
    ```sh
    make install
    ```
8. Ready to contribute!


## Issues

### Reporting Issues: 

If you find a bug or have a suggestion for an enhancement, please first check the issue tracker to see if it has already been reported. If it hasn't, feel free to open a new issue.

When creating an issue, use the templates provided in the .github/ISSUE_TEMPLATE directory. Fill out all the required fields.

## Pull Requests

### Branching

Always create a branch specific to the issue you are working on. Branch names should be descriptive and start with the issue number if applicable.

### Commits 

Write clear, concise commit messages that follow the conventional commit format.

### Pull Requests

Before submitting a pull request, ensure your changes adhere to the project’s standards:
- Run all tests to ensure no existing functionality is broken.
- Add or update tests for any new functionality.
- Update documentation as necessary.

```bash
Copy code
poetry run ruff src/
poetry run pytest
```

Open a pull request using the template provided in **.github/pull_request_template.md**.
Link the issue your PR addresses in the description.

## Code Review

All submissions require review and approval by project maintainers.
Maintain a respectful and constructive tone during discussions.
Address all feedback appropriately.

## Code of Conduct

We are committed to fostering an open and welcoming environment. By participating, you
are expected to uphold this code. Please report unacceptable behavior to
bengineerdavis@gmail.com


## Further Help

If you need further assistance, please contact Ben Davis.

## Acknowledgements
Thank you for contributing to Sawmill, making it better for everyone!