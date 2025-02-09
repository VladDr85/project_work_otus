# Поднять контейнеры
docker_up:
 docker-compose up -d

# Запуск приложения
run:
 uvicorn main:app --reload

# Проверка стиля кода
lint:
 pylint $(git ls-files '*.py')

# Запуск тестов
test:
 pytest -s --cov --cov-report html --cov-fail-under 85

# alembic
# alembic. Накат всех миграций
alembic_up_all:
 alembic upgrade head

# alembic. Откат всех миграций
alembic_down_all:
 alembic downgrade base

# alembic. Создать миграцию
alembic_gen:
 alembic revision --autogenerate -m "comment_xxx"
