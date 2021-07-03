.PHONY: all clean lint type test test-cov

CMD:=poetry run
PYMODULE:=j5_zoloto
TESTS:=tests
EXTRACODE:=
GENERATEDCODE:=

all: type test lint

lint:
	$(CMD) flake8 $(PYMODULE) $(TESTS) $(GENERATEDCODE)
	$(CMD) flake8 --config=extracode.flake8 $(EXTRACODE)

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
