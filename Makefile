.PHONY: all clean docs docs-serve lint type test test-cov

CMD:=poetry run
PYMODULE:=j5_zoloto
TESTS:=tests
EXTRACODE:=examples/
SPHINX_ARGS:=docs/ docs/_build -n
GENERATEDCODE:=

all: type test lint

docs:
	$(CMD) sphinx-build $(SPHINX_ARGS)

docs-serve:
	$(CMD) sphinx-autobuild $(SPHINX_ARGS)

lint:
	$(CMD) flake8 $(PYMODULE) $(TESTS) $(EXTRACODE) $(GENERATEDCODE)

type:
	$(CMD) mypy $(PYMODULE) $(TESTS) $(EXTRACODE) $(GENERATEDCODE)

test:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS)

test-cov:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report html

test-ci:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report xml

isort:
	$(CMD) isort $(PYMODULE) $(TESTS) $(EXTRACODE)

clean:
	git clean -Xdf # Delete all files in .gitignore
