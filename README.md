
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

### For Users

1. Install pipx:
    ```sh
    pip install pipx
    ```
2. Install Sawmill with pipx:
    ```sh
    pipx install sawmill
    ```
3. You can now use Sawmill from the command line.

### For Developers

1. Install the [pnpm package manager](https://pnpm.io/installation).
2. Use [Visual Studio Code](https://code.visualstudio.com/download) with these plugins:
    - Required: [Markdown Preview Mermaid Support](https://marketplace.visualstudio.com/items?itemName=bierner.markdown-mermaid)
    - Recommended: [Mermaid Chart](https://marketplace.visualstudio.com/items?itemName=MermaidChart.vscode-mermaid-chart)
3. Clone the repository:
    ```sh
    git clone git@github.com:bengineerdavis/sawmill.git
    ```
    Or:
    ```sh
    git clone https://github.com/bengineerdavis/sawmill.git
    ```
4. Install pipx:
    ```sh
    pip install pipx
    ```
5. Use pipx to install Poetry:
    ```sh
    pipx install poetry
    ```
6. (Optional) Set up a virtual environment or let Poetry manage it.
7. Navigate to the Sawmill directory:
    ```sh
    cd sawmill
    ```
8. Install Sawmill locally in editable mode:
    ```sh
    pipx install -e .
    ```
9. Install project dependencies:
    ```sh
    make install
    ```
10. Ready to contribute!

## Usage

To use Sawmill, run:
```sh
sawmill [path/to/file] [sql command string]|[sql command from file.sql]
```
This command returns a pandas DataFrame with the selected columns and rows defined in the SQL script.
