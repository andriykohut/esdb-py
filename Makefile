run-esdb:
	docker-compose up -d eventstore.db

protoc:
	python -m grpc_tools.protoc \
		-I=protos \
		--python_out=esdb/generated \
		--grpc_python_out=esdb/generated \
		--mypy_out=esdb/generated protos/*.proto

	./scripts/fix_protoc_imports.py esdb/generated/*.py*


pretty:
	black .
	isort .

lint:
	black --check .
	isort --check-only .
	flake8 .