
# Sawmill

Simple, powerful data analysis and reporting for your logs.

## Motivation

The majority I've my work as a programmer and technical support engineer requires that I
read tens of thousands of lines of unstructured logs, error messages, and stack traces.
Analyzing these files is often a time-consuming and error-prone task where important error
messages are easy to lose. This becomes especially acute when dealing with larger log
files and a larger variety of troubleshooting resource to scan by eye. 

Traditional monitoring tools can add complexity and require extensive setup and training.

Improve debug tools tend to take a back set to performance and feature reques. 

### Challenge

How can we quickly and accurately get the necessary information from log files without adding complexity to our workflow?

### Implementation

Sawmill is a terminal tool that lets you use SQL commands to filter local log files, showing only the relevant lines.

### Benefits

- **Saves Time:** Quickly find relevant log entries.
- **Extensible:** Supports automation and various log formats.
- **Cross-Team Usability:** Helpful for different teams.
- **User-Friendly:** Potentially usable by customers.
- **Competitive:** Customizable rules and optimizations.
- **Easy Installation and Learning:** Uses familiar SQL.
- **Efficient:** Reduces log lines for easier sharing and searching.
- **Scalable:** Ready for larger log datasets as needs grow.

## Setup

### User Requirements

Before a user begins using the application, they must meet following requirements:

- how to install Python projects locally -- we recommend using [pipx](https://pipx.pypa.io/stable/installation/) to install this project.
- a basic understanding of SQL and the command line.

It is recommended that the user is familiar with the project and it's processes by reading the README.md and other documentation.

### For Users

1. Install [pipx](https://pipx.pypa.io/stable/installation/):
    ```sh
    pip install pipx
    ```
2. Install Sawmill with pipx:
    ```sh
    pipx install sawmill
    ```
3. You can now use Sawmill from the command line.

### For Developers

See the [CONTRIBUTING.md](./CONTRIBUTING.md) file for more information.

## Usage

To use Sawmill, run:
```sh
sawmill [path/to/file] [sql command string]|[sql command from file.sql]
```
This command returns a pandas DataFrame with the selected columns and rows defined in the SQL script.
