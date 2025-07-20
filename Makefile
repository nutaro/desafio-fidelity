.PHONY: seed
seed:
	docker exec -i postgres psql -U postgres -d postgres < seed.sql

.PHONY: up-db
up-db:
	docker-compose up db -d

.PHONY: migration
migration:
	docker-compose up alembic -d

.PHONY: crawler
crawler:
	docker-compose up crawler -d

.PHONY: down
down:
	docker-compose down

.PHONY: logs
logs:
	docker container logs -f crawler
