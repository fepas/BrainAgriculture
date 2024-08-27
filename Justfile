COMPOSE_ENGINE := "docker compose"
PYTHON_VERSION_VENV := "python3.12"
VENV_BIN := "venv/bin"
API_CONTAINER := "brain_ag_api"

all: venv run-start

clean:
	{{COMPOSE_ENGINE}} down 
	rm -rf venv && sudo rm -rf tmp && rm -rf __pycache__

venv: 
	{{PYTHON_VERSION_VENV}} -m venv venv
	{{VENV_BIN}}/pip install --upgrade pip
	{{VENV_BIN}}/pip install -r requirements.txt

run-start: 
	{{COMPOSE_ENGINE}} up

run-down: 
	{{COMPOSE_ENGINE}} down 

run-build:	
	{{COMPOSE_ENGINE}} down 
	{{COMPOSE_ENGINE}} build

run-build-start: run-build run-start

run-docker-bash: 
	docker exec -it {{API_CONTAINER}} bash

run-django-shell:
	docker exec -it {{API_CONTAINER}} python manage.py shell

run-django-migrate: 
	docker exec -it {{API_CONTAINER}} python manage.py migrate

run-django-makemigrations: 
	docker exec -it {{API_CONTAINER}} python manage.py makemigrations

run-django-create-admin:
	docker exec -it {{API_CONTAINER}} bash -c "\
		DJANGO_SUPERUSER_PASSWORD=admin \
		python manage.py createsuperuser \
		--username admin \
		--email admin@example.com \
		--noinput"

run-fixtures:
	docker exec -it {{API_CONTAINER}} python manage.py loaddata api/fixtures/crops_fixture.json
	docker exec -it {{API_CONTAINER}} python manage.py loaddata api/fixtures/ruralproducers_fixture.json
	
run-set-db: run-django-migrate run-django-create-admin run-fixtures

run-test:
	docker exec -it {{API_CONTAINER}} python manage.py test api/tests

run-lint:
	black --check .
	isort --check-only .
	flake8

