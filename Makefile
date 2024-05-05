COMPOSE=docker compose
FEED=$(COMPOSE) run --rm runfeed

build:
	$(COMPOSE) build
start:
	$(COMPOSE) up -d
stop:
	$(COMPOSE) down
logs:
	$(COMPOSE) logs --follow --tail 1000
local-setup:
	${COMPOSE} up redis -d
local:
	bash docker-entrypoint.sh local