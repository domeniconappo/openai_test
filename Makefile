PROJECT_NAME := openai-test
DOCKER_COMPOSE := docker-compose -f docker-compose.yml
RUN := $(DOCKER_COMPOSE) run --rm api poetry run
MANAGE := $(RUN) python manage.py


build:
	docker build --tag $(PROJECT_NAME) --target production ./

# Development
build-dev:
	docker build --no-cache --tag $(PROJECT_NAME)-dev --target development ./

shell:
	${DOCKER_COMPOSE} run --rm api bash
	$(DOCKER_COMPOSE) stop

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

restart:
	$(DOCKER_COMPOSE) restart


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

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean: clean-pyc clean-build

# Formatting and Linting
format:
	$(RUN) isort .
	$(RUN) black .
	$(DOCKER_COMPOSE) stop

lint:
	$(RUN) flake8 .
	$(DOCKER_COMPOSE) stop

format: black isort

.PHONY: build-dev up down restart makemigrations migrate createsuperuser test clean-pyc clean-build clean black isort lint format
