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
