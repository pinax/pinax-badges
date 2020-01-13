all: init test

init:
	python setup.py develop
	pip install tox coverage

test:
	coverage erase
	tox --parallel
	coverage html
