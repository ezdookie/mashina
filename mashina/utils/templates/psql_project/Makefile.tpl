APP_NAME = {{ project_name }}


init:
	make migrate

rebuild:
	docker-compose down
	docker-compose build
	docker-compose up -d

pytest:
	docker-compose exec api pytest -s

logs:
	docker-compose logs -f

makemigrations:
	docker-compose exec api $(APP_NAME) makemigrations --message="${name}"

migrate:
	docker-compose exec api $(APP_NAME) migrate

delete-versions:
	sudo rm -rf api/${APP_NAME}/alembic/versions/*

create-app:
	docker-compose exec api $(APP_NAME) createapp ${singular} ${plural} ${APP_NAME}.apps
	sudo chown -R $$USER:$$USER api/${APP_NAME}/apps/${plural}/

cp-packages:
	docker cp "$$(docker-compose ps -q api)":/usr/local/lib/python3.6/site-packages ./site-packages
