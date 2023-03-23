dev:
	poetry run flask --app page_analyzer.app:app run

lint:
	poetry run flake8 page_analyzer

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer.app:app

test:
	poetry run pytest -vv

all:
	db-create shema-load

db-create:
	createdb test_pg_analyzer || echo 'skip'

shema-load:
	psql test_pg_analyzer < database.sql