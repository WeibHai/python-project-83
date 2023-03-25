dev:
	poetry run flask --app page_analyzer.app:app run

lint:
	poetry run flake8 page_analyzer

install:
	poetry install

PORT ?= 8000
start:
	psql railway < database.sql; poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app

test: poetry run pytest -vv
