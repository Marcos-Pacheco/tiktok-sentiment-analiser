DOCKER_COMPOSE=docker compose
PROFILE=chrome
UID=$(shell id -u)
GID=$(shell id -g)

up:
	UID=$(UID) GID=$(GID) $(DOCKER_COMPOSE) --profile $(PROFILE) up -d
down:
	UID=$(UID) GID=$(GID) $(DOCKER_COMPOSE) --profile "*" down
restart:
	UID=$(UID) GID=$(GID) $(DOCKER_COMPOSE) restart
true-restart:
	UID=$(UID) GID=$(GID) $(DOCKER_COMPOSE) down && $(DOCKER_COMPOSE) up -d
build:
	UID=$(UID) GID=$(GID) $(DOCKER_COMPOSE) up --build
rebuild:
	UID=$(UID) GID=$(GID) $(DOCKER_COMPOSE) up --build
init:
	UID=$(UID) GID=$(GID) $(DOCKER_COMPOSE) exec app bash -c "mkdir -p vendor && pip install --no-cache-dir --target=./vendor -r requirements.txt"
start:
	UID=$(UID) GID=$(GID) $(DOCKER_COMPOSE) exec app python app.py
freeze:
	UID=$(UID) GID=$(GID) $(DOCKER_COMPOSE) exec app bash -c "echo '--index-url https://pypi.org/simple' > requirements.txt && echo '--find-links https://download.pytorch.org/whl/cpu' >> requirements.txt && pip freeze --path ./vendor >> requirements.txt"