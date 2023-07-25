PROJECT_NAME := openai_test
DOCKER_COMPOSE := docker-compose -f docker-compose.yml
MANAGE := $(DOCKER_COMPOSE) run --rm web python manage.py

build:
	docker build -t $(PROJECT_NAME) --target production

# Development
build-dev:
	docker build -t $(PROJECT_NAME)-dev --target development

up:
	$(DOCKER_COMPOSE_DEV) up -d

down:
	$(DOCKER_COMPOSE_DEV) down

restart:
	$(DOCKER_COMPOSE_DEV) restart

# Django Commands
makemigrations:
	$(MANAGE) makemigrations

migrate:
	$(MANAGE) migrate

createsuperuser:
	$(MANAGE) createsuperuser

# Testing
test:
	$(MANAGE) pytest

# Cleaning
clean-pyc:
	find . -name "*.pyc" -exec rm -f {} +

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

clean: clean-pyc clean-build

# Formatting and Linting
black:
	$(MANAGE) black .

isort:
	$(MANAGE) isort .

lint:
	$(MANAGE) flake8 .

format: black isort

.PHONY: build-dev up down restart makemigrations migrate createsuperuser test clean-pyc clean-build clean black isort lint format
