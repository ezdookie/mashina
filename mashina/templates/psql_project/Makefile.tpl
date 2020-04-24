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
	docker-compose exec api python manage.py makemigrations --message="${name}"

migrate:
	docker-compose exec api python manage.py migrate

delete-versions:
	sudo rm -rf api/${APP_NAME}/alembic/versions/*

create-app:
	docker-compose exec api python manage.py createapp ${singular} ${plural}
	sudo chown -R $$USER:$$USER api/${APP_NAME}/apps/${plural}/