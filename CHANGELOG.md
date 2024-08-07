# Changelog.md

source: [keep a changelog](https://keepachangelog.com/en/1.1.0/)

## [Unreleased]

## [0.11.0] - 2024-07-21

### Added

- Adds initial pre-commit hooks to the project for code formatting and linting
- Adds initial pre-commit-config.yaml config file
- Adds pre-commit ruff linter and formatter to the project, via the
  .pre-commit-config.yaml file for code quality and consistency

### Changed

- Refactors Makefile to include pre-commit hooks for code formatting and linting by
  consolidating the 'make lint' and 'make format' commands into a single 'make check'
- Updates CONTRIBUTING.md with instructions on how to install the pre-commit CLI tool to
  the user's local development environment

## [0.10.1] - 2024-07-11

### Changed

- Updates poetry.lock and pyproject.toml files to use 'typer[all]' instead of 'typer'
  for the CLI app library, which includes all optional dependencies for Typer,
  especially 'Rich' for better integrated CLI output formatting

## [0.10.0] - 2024-07-11

### Added

- Adds another SQL script, 'demo.sql' that eventually be a colletion of examples for the user to try when learning the tool and its potential

### Fixed

- Resolves merge conflicts from the 'create-initial-in-terminal-view-of-log-file-2024-07-09' feature branch into 'main'

### Changed

- Updates README.md further with a new Learn More section and better linking to sections where the context makes more sense
- The New README.md#learn-more- section now links to the 'how-it-works.md' and 'data-structure-notes.md' in the /docs sub-directory for additional useful references for the user and contributor

### Removed

- Updates .gitignore file to not capture '.DS_Store' files in the repository

## [0.9.0] - 2024-07-09

### Added

- Adds ruff 'make lint' and 'make format' commands to the Makefile
- Adds ruff.toml for ruff linting and formatting configurations
- Adds contributor requirements to CONTRIBUTING.md

## [0.8.0] - 2024-07-07

### Changed

- Updates README.md with more succinct and percise instructions for users and developers
- Moved all developer steps and requirements to the CONTRIBUTING.md file from the
  project's README.md file
- Refactors user requirements in the README.md file for simplicity and clarity -- focus
  on not presuming the user's experience level with Python projects

## [0.7.0] - 2024-07-02

### Added

- Introduces Mermaid.js charts into markdown docs
- New docs directory contains a breakdown of how parts of sawmill are designed
- A new cli interface allows for the user to read in files from the terminal
- Refactored the [RestructuredData class](./src/sawmill/restructured.py) with new `Entry` and
  `File` objects in [Entry.py](./src/sawmill/entry.py) improve readability in the RestructureData.read()
  method for contributors
- Makefile now automates the user and dev installation process of sawmill and its dependencies
- Initial cli tests for missing or incorrect file path
- sawmill CLI app can now read in SQL scripts ('.sql') files as well as SQL string commands

### Fixed

- All xdoctests pass for restructured.RestructuredData()
- All primary and foreign key relations between the df_entries, df_lines, and df_file tables work as intended
-

### Changed

- Removes artifacts created by pnpm and Node.js dependency management for mermaid via .gitignore
- README.md has been updated to included required/recommended Visual Studio code editor and plugins
- README.md has been updated to included the installation and use of pnpm Node.js dependency manager
- Updates [data-structure-notes.md](./docs/data-structure-notes.md) ER graph with accurate field names now produced
by the sawmill app
- Adds duckdb to poetry's user and dev dependencies that allows users direct SQL querying of files by Python

## [0.1.0] - 2024-06-09

### Added

- Initailizes the `sawmill` project
- Adds initial project files
- Adds SQLAlchemy, Pandas, pre-commit and Datasette to project dependencies

## [Template] - YYYY-MM-DD

### Added

### Fixed

### Changed

### Removed

### Security
