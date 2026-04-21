.PHONY: up down restart logs format lint setup

up:
	docker compose up --build -d
down:
	docker compose down -v
restart:
	docker compose down
	docker compose up --build -d
logs:
	docker compose logs -f
format:
	ruff format .
	ruff check --fix .
lint:
	ruff check .
setup:
	uv sync --all-groups
fill:
	docker compose exec api python -m api.fill_db 1000