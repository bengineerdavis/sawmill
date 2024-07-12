# Changelog.md

source: [keep a changelog](https://keepachangelog.com/en/1.1.0/)

## [Unreleased] 

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