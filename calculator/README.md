# Calculator

Simple Python calculator project. This repository contains a small `calculator` package, unit tests, coverage configuration, and a CI workflow.

**Quick Start**

Create and activate a virtual environment, then install the development dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional: install the package in editable mode so editors and tests can import it normally:

```bash
pip install -e .
```

**Project Layout**

- `calculator/` - Python package with calculator logic (`core.py`)
- `tests/` - Unit tests (`test_core.py`, `test_calculator.py`)
- `.github/workflows/ci.yml` - GitHub Actions CI workflow that runs tests
- `.coveragerc` - coverage.py configuration
- `requirements.txt` - development/test dependencies (includes `coverage`)
- `pyproject.toml` - project metadata (Poetry format)

**Usage**

From the project root:

```python
from calculator.core import add
print(add(2, 3))
```

**Run Tests**

Run the unittest test suite from the repository root:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

If tests in `tests/` cannot import the package in your editor, either install the package in editable mode (`pip install -e .`) or run tests from the repository root so the tests' `sys.path` adjustments work.

**Code Coverage**

This project uses `coverage.py` to measure test coverage. To run coverage and require 100%:

```bash
# install coverage (if needed)
pip install --user coverage

# run tests under coverage
coverage run -m unittest discover -s tests -p 'test_*.py'

# show coverage and fail if below 100%
coverage report -m --fail-under=100

# (optional) generate an HTML report
coverage html
# HTML report is written to `htmlcov/` (this folder is ignored by git)
```

**CI (GitHub Actions)**

A CI workflow is included at `.github/workflows/ci.yml`. It sets up Python, installs dependencies, and runs the test suite. To enforce coverage in CI add steps to install `coverage` and run `coverage report -m --fail-under=100`.

Example snippet to add to CI:

```yaml
- name: Install coverage
  run: pip install coverage

- name: Run coverage
  run: coverage run -m unittest discover -s tests -p 'test_*.py'

- name: Check coverage
  run: coverage report -m --fail-under=100
```

**Repository notes**

- A backup branch named `backup-full-repo` was pushed to the remote before making destructive changes. If you need to restore the previous repository root, you can run:

```bash
git fetch origin
git push origin backup-full-repo:main
```

- The remote `main` branch was replaced with a branch derived from the `calculator/` folder (the `calc-only` subtree). If you prefer the full-repo state, use the backup branch above.

**Cleaning up local temporary branches**

If you want to remove temporary branches created during the subtree operation:

```bash
git checkout main
git branch -D calc-only
```

If you have questions or want me to add CI coverage enforcement or make the package installable with `setup.cfg`/`pyproject` metadata for editable installs, tell me which option you prefer.
# Calculator

Simple Python calculator project created as a starter GitHub repository.

## Quick start

Install dependencies (recommended in a virtual environment):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run tests:

```bash
python3 -m unittest discover -v
```

## Project layout

- `calculator/` - Python package with calculator logic
- `tests/` - Unit tests
- `pyproject.toml` - Project metadata

## Usage

From the project root, run Python and import the library:

```python
from calculator import add
print(add(2, 3))
```

## Running tests

Use the following command to run the unit tests:

```bash
python3 -m unittest discover -v
```
