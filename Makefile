all: init docs test

init:
	python setup.py develop
	pip install detox coverage mkdocs

test:
	coverage erase
	detox
	coverage html

docs:
	mkdocs build

.PHONY: docs
