# Contributing to Sawmill

Thank you for your interest in contributing to Sawmill! This document provides guidelines for making contributions to the project. By participating in this project, you agree to abide by its terms.

## Getting Started

Before you begin:
- Ensure you have Python 3.11 installed. Sawmill is developed with this version.
- Familiarize yourself with the project by reading the README.md and other documentation.
- Set up the project on your local machine. Here’s how:

```bash
git clone https://github.com/USERNAME/sawmill.git
cd sawmill
curl -sSL https://install.python-poetry.org | python3 -
poetry install
```

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

We are committed to fostering an open and welcoming environment. By participating, you are expected to uphold this code. Please report unacceptable behavior to bengineerdavis@gmail.com.

## Further Help

If you need further assistance, please contact Ben Davis.

## Acknowledgements
Thank you for contributing to Sawmill, making it better for everyone!