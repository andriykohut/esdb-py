run-esdb:
	docker-compose up -d eventstore.db

protoc:
	python -m grpc_tools.protoc \
		-I=protos \
		--python_out=esdb/generated \
		--grpc_python_out=esdb/generated \
		--mypy_out=esdb/generated protos/*.proto


pretty:
	black .
	isort .
