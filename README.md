# Sawmill

A collection of tools for easy parsing and analyzing of log files and stack trace data.

Sawmill is a Python package that allows users to query log files using SQL commands. It
is designed to be user-friendly and extensible, with the goal of saving time and
improving efficiency when working with log files.

## Learn more

* How to [install](#installation) and [usage](#usage) sawmill.
* How to [contribute](./CONTRIBUTING.md#contributing-to-sawmill) to the project.
* How it [works](./docs/how-it-works.md).
* How sawmill breaks down and represents your file as a [machine-searchable datatype](./docs/data-structure-notes.md) interally.

## Usage

To use Sawmill, run:

```sh
sawmill [path/to/file] [sql command string]|[sql command from file.sql]
```

This command returns a pandas DataFrame with the selected columns and rows defined in the SQL script.

## Installation

Please review and confirm the expected [prerequisites](#prerequisites)

1. Install sawmill on your local machine with [pipx](https://pipx.pypa.io/stable/installation/)

* While this can be done with Python's official installer, [pip], via your
   system-installed Python, it is **strongly** recommended to use pipx
* Install [pipx](https://pipx.pypa.io/stable/installation/):

2. Install Sawmill with pipx:

    ```sh
    pipx install sawmill
    ```

3. You can now use Sawmill from the command line. Check out the [Usage](#usage) section,
   next.

For common issues encountered during installation, please review the [Troubleshooting](#troubleshooting) section.

## Troubleshooting

### Prerequisites

1. Make sure that **Python** and it's dependency installer **pip**, are available on the
   user's local machine. Please refer to the first two sections in
   [Requirements for Installing Packages - Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/installing-packages/#requirements-for-installing-packages)

2. The user is expected to have a very basic understanding of, or willingness to learn, the
following: A modest amount of SQL, a _little_ bit about how to use the Unix command line

3. The user should already have [pipx](https://pipx.pypa.io/stable/installation/)
   installed on their local machine

_For those who wish to self-learn more about the topics above,
[Recommended Learning Resources](./docs/recommended-learning-resources.md) file._

## Contributing

Thank you for your interest in contributing to Sawmill!

Please see the [CONTRIBUTING.md](./CONTRIBUTING.md) file for more information -- NOT REQUIRED
for general usage!!

## Usage

```bash
# command returns pandas DataFrame with user-select columns and rows defined in the SQL script

sawmill [path/to/file] [sql command string]|[sql command from file.sql]
