.PHONY: help
.DEFAULT_GOAL := help

SCRIPT := t3reports
PYTHON := $$(pyenv which python)
PY_VERSION := 3.12.1
VENV_NAME := sawmill-dev

INSTALL_DIR := ../

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.PHONY: clean clean-venv
clean: clean-venv  ## cleans up all python caching and other artifact files, including removal of the local venv for this directory
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name '*.log' -exec rm -fr {} +

clean-venv:  # removes auto-activation of venv and then deletes the venv T3RAP environment
	if [ -f .python-version ]; then \
    	printf '.python-version found!\n\n\n' && \
		pyenv local --unset && \
		pyenv virtualenv-delete -f $(VENV_NAME); \
	else \
		echo '.python-version not found!'; \
	fi


.PHONY: check
check:  # confirms that a pyenv virtual environment is activated
	@echo "check for successfully created and activated Python venv or stopping make command ..."
	if [ ! -f .python-version ]; then \
    	echo '.python-version not found! .python-version is missing -- pyenv virtual environment is not activated' && \
		exit 1; \
	else \
		echo 'Confirmed that a pyenv Python virtual environment is activated!'; \
	fi


.PHONY: update
update: check  # use to update venv's Python dependencies and auxiliary tools; also updates user-wide pipx installation of t3reports
	@echo "using pipx to update poetry"
	pipx upgrade poetry

	@echo "Updating requirements with poetry"
	poetry update


.PHONY: venv venv-update install
venv:  # create a fresh, dedicated venv for the T3RAP local repo and t3report app with pyenv-virtualenv plugin
	@echo "Making sure that Python versiom $(PY_VERSION) has been installed by pyenv!"
	pyenv install --skip-existing $(PY_VERSION)
	
	@echo "Creating a fresh virtualenv is install for the $(VENV_NAME) directory with Python version $(PY_VERSION)"
	pyenv virtualenv $(PY_VERSION) $(VENV_NAME)
	
	@echo "Assigning the $(VENV_NAME) venv to the current directory"
	pyenv local $(VENV_NAME)

venv-update:  check # update pip and other dependency manage tools installed within the virtual environment
	@echo "Making sure both pip and pip-tools are installed and up-to-date in the virtual environment"
	pip install --upgrade pip pip-tools

install: clean tools venv venv-update update  ## fresh developer installation of the t3reports app and Python dependencies


.PHONY: compile upgrade
compile:  # compile an updated requirements.txt from requirements.in; should only be used when updating dependencies in setup.cfg
	@echo "Compiling a new requirements.txt based on requirements.in with pip-compile"
	pip-compile --no-emit-index-url -v

upgrade: tools compile update  ## use when updating dependencies (or their versions) in setup.cfg


.PHONY: ssh
ssh:  # install user's ssh key and save to system clipboard to put in GitHub

