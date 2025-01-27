### COLORS ###
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[0;33m
BLUE = \033[0;34m
MAGENTA = \033[0;35m
CYAN = \033[0;36m
RESET = \033[0m

### VARIABLES ###
IMG = snow-crash-solver
CONTAINER = snow-crash-solver
APP_DIR = /snow-crash
RM = rm -f
IP = 192.168.1.14
PORT = 4242
SOLUTIONS = solutions.json
LEVEL ?= ALL
# Checkers
IMAGE_EXISTS := $(shell docker images -q $(IMG))
CONTAINER_EXISTS := $(shell docker ps -q -f name=$(CONTAINER))
CONTAINER_IS_RUNNING := $(shell docker inspect -f '{{.State.Running}}' $(CONTAINER) 2>/dev/null)

config:
	@./config.sh
	@make -s build
	@make -s run

build:
	@echo "$(CYAN)Building $(IMG) image...$(RESET)"
	@docker build -t $(IMG) .

build-no-cache:
	@echo "$(CYAN)Building $(IMG) image from scratch...$(RESET)"
	@docker build --no-cache -t $(IMG) .

solve:
	@echo "$(CYAN)Solving level(s) $(LEVEL)...$(RESET)"
	@if [ -z "$(CONTAINER_IS_RUNNING)" ]; then \
		make -s run; \
	fi
	@docker exec $(CONTAINER) /bin/bash -c "export LEVEL=$(LEVEL) && python solver.py"

run:
	@if [ -z "$(IMAGE_EXISTS)" ]; then \
		make -s build; \
	fi
	@echo "$(CYAN)Starting $(CONTAINER) container...$(RESET)"
	@docker run \
		-d \
		--rm \
		--name $(CONTAINER) \
		-v $(PWD):$(APP_DIR) \
		--network host \
		-e IP=$(IP) \
		-e PORT=$(PORT) \
		-e LEVEL=$(LEVEL) \
		$(IMG)
	@echo "$(GREEN)$(CONTAINER) container is running.$(RESET)"

stop:
	@echo "$(CYAN)Stopping $(CONTAINER) container...$(RESET)"
	@if [ ! -z "$(CONTAINER_IS_RUNNING)" ]; then \
		docker stop $(CONTAINER); \
	fi
	@echo "$(RED)$(CONTAINER) container has been stopped.$(RESET)"

clean: stop
	@echo "$(CYAN)Removing $(CONTAINER) container...$(RESET)"
	@docker rm $(CONTAINER) || true

fclean: clean
	@echo -n "$(CYAN)Removing $(IMG) image... "
	@docker rmi $(IMG) || true
	@echo "done$(RESET)"
	@echo -n "$(CYAN)Removing $(SOLUTIONS) file... "
	@$(RM) $(SOLUTIONS)
	@echo "done$(RESET)"

re: clean build run

shell:
	@echo "$(CYAN)Starting shell in $(CONTAINER) container...$(RESET)"
	@docker exec -it $(CONTAINER) /bin/bash

logs:
	@echo "$(CYAN)Displaying logs of $(CONTAINER) container...$(RESET)"
	@docker logs $(CONTAINER)

logs-follow:
	@echo "$(CYAN)Displaying logs of $(CONTAINER) container...$(RESET)"
	@docker logs -f $(CONTAINER)

help:
	@echo "$(CYAN)Usage:$(RESET)"
	@echo ""
	@echo "$(YELLOW) make config$(RESET)          - Configure and run the container"
	@echo ""
	@echo "$(YELLOW) make solve$(RESET)           - Solve the level(s)"
	@echo "    $(MAGENTA)LEVEL=XX$(RESET)         - Specify the level(s) to solve"
	@echo "    $(MAGENTA)LEVEL=ALL$(RESET)        - Solve all levels"
	@echo "    $(MAGENTA)LEVEL=XX-YY$(RESET)      - Solve levels from XX to YY"
	@echo "    $(MAGENTA)LEVEL=XX,YY$(RESET)      - Solve levels XX and YY"
	@echo "    $(MAGENTA)LEVEL=XX,YY-ZZ$(RESET)   - Solve levels XX, YY and ZZ"
	@echo "    $(MAGENTA)LEVEL=MANDATORY$(RESET)  - Solve all mandatory levels"
	@echo "    $(MAGENTA)LEVEL=BONUS$(RESET)      - Solve all bonus levels"
	@echo ""
	@echo "$(YELLOW) make build$(RESET)          - Build the image"
	@echo "$(YELLOW) make build-no-cache$(RESET) - Build the image from scratch"
	@echo "$(YELLOW) make run$(RESET)            - Run the container"
	@echo "$(YELLOW) make stop$(RESET)           - Stop the container"
	@echo "$(YELLOW) make clean$(RESET)          - Remove the container"
	@echo "$(YELLOW) make fclean$(RESET)         - Remove the image"
	@echo "$(YELLOW) make re$(RESET)             - Rebuild the image and run the container"
	@echo "$(YELLOW) make shell$(RESET)          - Start a shell in the container"
	@echo "$(YELLOW) make logs$(RESET)           - Display the logs of the container"
	@echo "$(YELLOW) make logs-follow$(RESET)    - Display the logs of the container and follow them"

.PHONY: build run stop clean fclean re logs logs-follow