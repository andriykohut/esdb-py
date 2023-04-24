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
	pdm run black .
	pdm run isort .

lint:
	pdm run black --check .
	pdm run isort --check-only .
	pdm run flake8 .
	pdm run mypy .

test:
	pdm run pytest --cov esdb

test-ci:
	pdm run pytest --cov esdb --cov-report=xml

html-cov: test
	pdm run coverage html
	open htmlcov/index.html

cleanup:
	docker-compose down -v
	rm -rf dist
	rm -rf htmlcov