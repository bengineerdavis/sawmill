
# Sawmill

Cut through the noise in your log and stack trace files through simple, beautiful, 
powerful debugging data analysis and reporting.

## Motivation

As programmer debugging both work and personal projects, I will inevitably have to read
tens of thousands of lines of unstructured logs, error messages, and stack traces.
Often, only a dozen or less lines are relevant to the problem at hand.

In order to get to those lines, I am faced with a manual, time-consuming and error-prone
scans of logs and stack traces. Established alternatives, like traditional monitoring
logging tools can add considerable complexity and require extensive setup and training.
These tools also force the user to learn a new query language, adding another layer to
the learning curve while trapping companies in vendor lock-in.

Altogether, these costs I often find prohibitively complex to launch small projects or
for personal use, or too expensive to scale and maintain as teams grow.

Wouldn't it be great if we could easily query our logs and focus only on the important lines,

### Challenge

How can we quickly and accurately get the necessary information from log files without
adding complexity to our workflow?

How to create a powerful grep-like user-friendly, portable, easy to scale usage through training and accessible to a wider audience?

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

### For Users

1. Install sawmill on your local machine with [pipx](https://pipx.pypa.io/stable/installation/)

- While this can be done with Python's official installer, [pip], via your
   system-installed Python, it is **strongly** recommended to use pipx
- Install [pipx](https://pipx.pypa.io/stable/installation/):

2. Install Sawmill with pipx:
    ```sh
    pipx install sawmill
    ```
3. You can now use Sawmill from the command line. Check out the [Usage](#usage) section, next.

### For Who Want to Contributor

Thank you for your interest in contributing to Sawmill!

Please see the [CONTRIBUTING.md](./CONTRIBUTING.md) file for more information -- NOT REQUIRED
for general usage!!

## Usage

To use Sawmill, run:
```sh
sawmill [path/to/file] [sql command string]|[sql command from file.sql]
```
This command returns a pandas DataFrame with the selected columns and rows defined in the SQL script.


