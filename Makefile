DB_DC_FILE = docker_compose/database.yaml
DB_CONTAINER = "project-db"

BACKEND_DC_FILE = docker_compose/backend.yaml
BACKEND_CONTAINER = "backend-app"
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


# BACKEND APP
# ________________________________
.PHONY: backend-image
backend-image:
	docker build -t backend_app .

.PHONY: backend
backend:
	docker compose -f ${BACKEND_DC_FILE} -f ${DB_DC_FILE} up -d

.PHONY: backend-logs
backend-logs:
	docker logs ${BACKEND_CONTAINER} -f

.PHONY: backend-stop
backend-stop:
	docker compose -f ${BACKEND_DC_FILE} -f ${DB_DC_FILE} down
.PHONY: migrate
migrate:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} migrate

.PHONY: migrations
migrations:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} makemigrations

.PHONY: superuser
superuser:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} createsuperuser

.PHONY: collectstatic
collectstatic:
	${EXEC} ${APP_CONTAINER} ${MANAGE_PY} collectstatic
