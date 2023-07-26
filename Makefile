PROJECT_NAME := openai-test
DOCKER_COMPOSE := docker-compose -f docker-compose.yml
RUN := $(DOCKER_COMPOSE) run --rm api poetry run
RUN_NODEPS := $(DOCKER_COMPOSE) run --no-deps --rm api poetry run
MANAGE := $(RUN) python manage.py


build:
	docker build --progress=plain --tag $(PROJECT_NAME) --target production ./

# Development
build-dev:
	docker build --no-cache --progress=plain --tag $(PROJECT_NAME)-dev --target development ./

shell:
	${DOCKER_COMPOSE} run --rm api bash
	$(DOCKER_COMPOSE) stop

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) restart

reset:
	$(DOCKER_COMPOSE) down -v

# Django Commands
makemigrations:
	$(MANAGE) makemigrations
	$(DOCKER_COMPOSE) stop

migrate:
	$(MANAGE) migrate
	$(DOCKER_COMPOSE) stop

createsuperuser:
	$(MANAGE) createsuperuser
	$(DOCKER_COMPOSE) stop

# Testing
test:
	$(RUN) pytest
	$(DOCKER_COMPOSE) stop

# Cleaning
clean-pyc:
	find . -name "*.pyc" -exec rm -f {} +


# Formatting and Linting
format:
	$(RUN_NODEPS) isort .
	$(RUN_NODEPS) black .
	$(DOCKER_COMPOSE) stop

type-check:
	$(RUN_NODEPS) mypy .
	$(DOCKER_COMPOSE) stop

.PHONY: build build-dev up down reset restart makemigrations migrate createsuperuser test clean-pyc clean-build clean black isort type-check format
