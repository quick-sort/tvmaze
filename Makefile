
start_dev:
	docker-compose -f docker-compose-dev.yml up -d
	docker logs -f api-service

stop_dev:
	docker-compose -f docker-compose-dev.yml down

start:
	docker-compose -f docker-compose.yml up -d

stop:
	docker-compose -f docker-compose.yml stop

image:
	poetry export -f requirements.txt --output requirements.txt
	docker build -t api-service .

gen_sample:
	bash -x ./scripts/gen_sample_db.sh

test:
	bash -x ./scripts/test.sh
