# Development Information

## Install need tools:
Run this in the terminal:

`pip install -r .\requirements_dev.txt`

`pip install -e .`

## To run tests:
Run this in the terminal:

`pytest`


## To run flake8:
Run this in the terminal:

`flake8 src`


## To run mypy:
Run this in the terminal:

`mypy src`

## To run tox:
Run this in the terminal:

`tox`

---
## To build package and push update:
Run this in the terminal:

`py -m build`

`twine upload dist/*`

## To creating/update badges:

**Test:**

`pytest --junitxml=reports/junit/junit.xml`

`genbadge tests -o -> ./tests/badges/tests-badge.svg`

**Coverange:**

`genbadge coverage -o -> ./tests/badges/coverage-badge.svg`

**flake8:**

`flake8 src  --exit-zero --format=html --htmldir ./reports/flake8 --statistics --tee --output-file flake8stats.txt`

`genbadge flake8 -o -> ./tests/badges/flake8-badge.svg`


