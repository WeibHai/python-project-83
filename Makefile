PORT ?= 8000

dev:
	poetry run flask --app page_analyzer.app:app run

lint:
	poetry run flake8 page_analyzer

install:
	poetry install

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app

test: poetry run pytest -vv

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml