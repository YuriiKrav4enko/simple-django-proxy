DB_DC_FILE = docker_compose/database.yaml
DB_CONTAINER = "project-db"

# DATABASE
# ________________________________
.PHONY: db
db:
	docker compose -f ${DB_DC_FILE} up -d

.PHONY: db-stop
db-stop:
	docker compose -f ${DB_DC_FILE} down

.PHONY: db-logs
db-logs:
	docker logs ${DB_CONTAINER} -f
