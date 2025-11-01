# FastAPI-Calculator
The simple calculator based on FastAPI framework

## What you need for running the App
Git, Python 3, Pipenv, Docker

## How to get and run the App

* Clone the App repository
`git clone https://github.com/msydor3nko/FastAPI-Calculator.git`

* Enter to the 'FastAPI-Calculator' directory
`cd FastAPI-Calculator`

* Activate virtual environment
`pipenv shell`

* Install all needed libraries from 'Pipfile'
`pipenv install --dev`

* Run MongoDB into Docker container using 'docker-compose.yml'
`docker-compose up`

* Run ASGI server with working App
`uvicorn main:app --reload`

* Follow by provided link ('http://127.0.0.1:8000/docs' by default) to interact with the App API

* Also, you can testing the App using PyTest as in the comand bellow
`pytest -v`
