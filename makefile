SERVICE_PORT = 8080

#include .env
export

run:
	poetry run bash start.sh

build-image:
	docker build -t front-rotasegura .

run-docker:
	docker run -p 8501:8501 front-rotasegura
