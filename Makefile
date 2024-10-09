DOCKER_COMPOSE=docker compose
profile=chrome

up:
	$(DOCKER_COMPOSE) --profile $(profile) up -d
down:
	$(DOCKER_COMPOSE) --profile "*" down
restart:
	$(DOCKER_COMPOSE) restart
true-restart:
	$(DOCKER_COMPOSE) down && $(DOCKER_COMPOSE) up -d
build:
	$(DOCKER_COMPOSE) up --build
rebuild:
	$(DOCKER_COMPOSE) up --build
init:
	$(DOCKER_COMPOSE) exec app pip install -r requirements.txt
start:
	$(DOCKER_COMPOSE) exec app python app.py
