# Короткие команды для повседневной работы. Запуск: make <цель>
# Все django-команды выполняются ВНУТРИ контейнера web.

.PHONY: up down logs shell migrate makemigrations superuser test check

up:            ## собрать и поднять всё
	docker compose up --build

down:          ## остановить (данные базы сохраняются)
	docker compose down

logs:          ## смотреть логи
	docker compose logs -f web

shell:         ## django shell внутри контейнера
	docker compose exec web python manage.py shell

migrate:
	docker compose exec web python manage.py migrate

makemigrations:
	docker compose exec web python manage.py makemigrations

superuser:     ## создать админа
	docker compose exec web python manage.py createsuperuser

test:
	docker compose exec web python manage.py test

check:         ## проверки Django + что все миграции созданы
	docker compose exec web python manage.py check
	docker compose exec web python manage.py makemigrations --check --dry-run
