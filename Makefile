IMG = snow-crash-solver
CONTAINER = snow-crash-solver

build:
	docker build -t $(IMG) .

build-no-cache:
	docker build --no-cache -t $(IMG) .

run:
	docker run -it --rm --name $(CONTAINER) $(IMG) 

stop:
	docker stop $(CONTAINER)

clean: stop
	docker rm $(CONTAINER) || true

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