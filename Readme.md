# Django Boilerplate with Docker Compose, Makefile, and PostgreSQL

This is a simple proxy Django project with using Docker Compose, Makefile, and PostgreSQL.

## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## How to Use

1. **Clone the repository:**


2. To run project locally build project imake with `make backend-image`
and up aplication with `make backend`.

3. Create a superuser with `make superuser`.

4. Use `make backend-stop` command to down app.

Also you can up only database `make db` and run project locally with `./manage.py runserver`.


### Implemented Commands

* `make backend-image` - build app docker image
* `make backend` - up application and database/infrastructure
* `make backend-logs` - follow the logs in app container
* `make backend-stop` - down application and all infrastructure
* `make db` - up only storages. you should run your application locally for debugging/developing purposes
* `make db-logs` - foolow the logs in storages containers
* `make db-stop` - down all infrastructure

### Most Used Django Specific Commands

* `make migrations` - make migrations to models
* `make migrate` - apply all made migrations
* `make collectstatic` - collect static
* `make superuser` - create admin user