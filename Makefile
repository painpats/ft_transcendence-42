DOCKER_CMD = docker
COMPOSE_CMD = docker compose
COMPOSE_FILE = docker-compose.yml

all: build up

build:
	$(COMPOSE_CMD) -f $(COMPOSE_FILE) build

up: build
	$(COMPOSE_CMD) -f $(COMPOSE_FILE) up -d

down:
	sudo rm -rf django/website/staticfiles/*
	sudo rm -rf django/website/mediafiles/*
	$(COMPOSE_CMD) -f $(COMPOSE_FILE) down -v --rmi all

re: down up

list:
	$(DOCKER_CMD) ps -a
	$(DOCKER_CMD) volume ls
	$(DOCKER_CMD) image ls
	$(DOCKER_CMD) network ls