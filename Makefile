IMG = snow-crash-solver
CONTAINER = snow-crash-solver

build:
	docker build -t $(IMG) .

run:
	docker run -it --rm $(IMG) --$(CONTAINER) 

stop:
	docker stop $(CONTAINER)

clean: stop
	docker rm $(CONTAINER) || true

fclean: clean
	docker rmi $(IMG) || true

.PHONY: build run stop clean fclean