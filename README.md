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

### Developers

1. Clone the repository
```sh
# if the user has ssh access to GitHub
git clone git@github.com:bengineerdavis/sawmill.git
```

for everyone else ...

```sh
git clone https://github.com/bengineerdavis/sawmill.git
```
2. Install [`pipx`](https://github.com/pypa/pipx?tab=readme-ov-file#install-pipx)
3. Use `pipx` to install `poetry`
```sh
pipx install poetry
```
4. OPTIONAL: the user may set up their own `virtual environment` or let `poetry` to manage it for them
5. Navigate into the new local `sawmill` directory
```sh
cd sawmill
```
6. Use pipx to make an editable installation of sawmill on the user's local machine
```sh
pipx install -e .
```
7. Install project dependencies 
```sh
make install
```
6. Ready to contribute!