IMG = snow-crash-solver
CONTAINER = snow-crash-solver
APP_DIR = /snow-crash
RM = rm -f
IP = 192.168.1.10
PORT = 4242

build:
	docker build -t $(IMG) .

build-no-cache:
	docker build --no-cache -t $(IMG) .

run:
	docker run \
		-it \
		--rm \
		--name $(CONTAINER) \
		-v $(PWD):$(APP_DIR) \
		-e IP=$(IP) \
		-e PORT=$(PORT) \
		$(IMG) 

stop:
	docker stop $(CONTAINER)

clean: stop
	docker rm $(CONTAINER) || true
	$(RM) level02/resources/level02.pcap

fclean: clean
	docker rmi $(IMG) || true

re: clean build run

shell:
	docker exec -it $(CONTAINER) /bin/bash

logs:
	docker logs $(CONTAINER)

logs-follow:
	docker logs -f $(CONTAINER)

.PHONY: build run stop clean fclean re logs logs-follow