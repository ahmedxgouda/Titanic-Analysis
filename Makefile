run:
	@DOCKER_BUILDKIT=1 COMPOSE_BAKE=1 docker compose -f ./docker/docker-compose.yaml up --build --remove-orphans
