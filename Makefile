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
IP = 192.168.1.10
PORT = 4242

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

run:
	@echo "$(CYAN)Running $(IMG) container...$(RESET)"
	@docker run \
		-it \
		--rm \
		--name $(CONTAINER) \
		-v $(PWD):$(APP_DIR) \
		-e IP=$(IP) \
		-e PORT=$(PORT) \
		$(IMG) 

stop:
	@echo "$(CYAN)Stopping $(CONTAINER) container...$(RESET)"
	@docker stop $(CONTAINER)

clean: stop
	@echo "$(CYAN)Removing $(CONTAINER) container...$(RESET)"
	@docker rm $(CONTAINER) || true

fclean: clean
	@echo "$(CYAN)Removing $(IMG) image...$(RESET)"
	@docker rmi $(IMG) || true

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
	@echo " make [config]		- Configure and run the container"
	@echo " make build		- Build the image"
	@echo " make build-no-cache	- Build the image from scratch"
	@echo " make run		- Run the container"
	@echo " make stop		- Stop the container"
	@echo " make clean		- Remove the container"
	@echo " make fclean		- Remove the image"
	@echo " make re		- Rebuild the image and run the container"
	@echo " make shell		- Start a shell in the container"
	@echo " make logs		- Display the logs of the container"
	@echo " make logs-follow	- Display the logs of the container and follow them"

.PHONY: build run stop clean fclean re logs logs-follow