
## nbmeta/Makefile

.PHONY: default install nb test test-all run-all html-index readme-index \
	index html-all clean clean-html clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

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

mkfile_path := $(abspath $(lastword $(MAKEFILE_LIST)))
mkfile_dir = $(shell dirname $(mkfile_path))

default: help

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test clean-html ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint: ## check style with flake8
	flake8 nbmeta tests

test: ## run tests quickly with the default Python
	pytest

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source nbmeta -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/nbmeta.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ nbmeta
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install


install-notebook:
	# pip install virtualenvwrapper
	# mkvirtualenv <name>
	# bash ./install.sh
	pip install jupyterlab


nb:
	jupyter notebook --ip=127.0.0.1 --notebook-dir=.

lab:
	jupyter lab --ip=127.0.0.1 --notebook-dir=.

test: test-all

test-all-nbs:
	find $(mkfile_dir) -name '*.ipynb' -exec jupyter nbconvert --to notebook --execute {} \;

run-all-nbs:
	find $(mkfile_dir) -name '*.ipynb' -exec jupyter nbconvert --to notebook --execute {} \;


html-index:
	python ./makeindex.py \
		--html \
		--nbviewer-url="https://nbviewer.org/github/westurner/nbmeta/blob/main/" \
		--binderhub-url="https://mybinder.org/v2/gh/westurner/nbmeta/main?labpath=" \
		> ./index.html

readme-index:
	python ./makeindex.py \
		--readme \
		--nbviewer-url="https://nbviewer.org/github/westurner/nbmeta/blob/main/" \
		--binderhub-url="https://mybinder.org/v2/gh/westurner/nbmeta/main?labpath=" \
		> ./README.md

index: html-index readme-index

html-all:
	find . -name '*.ipynb' -print0 | while read -d $$'\0' file; \
	do \
		if [ ! -z `echo $$file | grep -v '.ipynb_checkpoints/'` ]; \
			cd $(mkfile_dir)/`dirname "$$file"`; \
			ipython nbconvert "`basename $$file`" --to html; \
			htmlfile=`echo "$$file" | sed 's/.ipynb$$/.html/g'` ; \
		fi \
	done;
	$(MAKE) html-index
	$(MAKE) readme-index


clean-html:
	rm index.html
	find $(mkfile_dir) -name '*.html' -print0 | xargs -0 rm -fv
