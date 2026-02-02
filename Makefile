set_role:
	poetry run python -m scripts.set_role
docker.up:
	docker compose up -d
docker.down:
	docker compose down
start:
	docker compose up --build