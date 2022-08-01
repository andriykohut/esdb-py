run-esdb:
	docker-compose up -d

protoc:
	python -m grpc_tools.protoc \
		-I=protos \
		--python_out=esdb/generated \
		--grpc_python_out=esdb/generated \
		--mypy_out=esdb/generated protos/*.proto

	./scripts/fix_protoc_imports.py esdb/generated/*.py*


pretty:
	poetry run black .
	poetry run isort .

lint:
	poetry run black --check .
	poetry run isort --check-only .
	poetry run flake8 .
	poetry run mypy ./esdb

test:
	poetry run pytest --cov esdb

test:
	poetry run pytest --cov esdb --cov-report=xml

html-cov: test
	poetry run coverage html
	open htmlcov/index.html

cleanup:
	docker-compose down -v
	rm -rf dist
	rm -rf htmlcov