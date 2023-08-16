start-api:
	docker-compose up api

start-frontend:
	docker-compose up frontend

down:
	docker-compose down

destroy-api:
	docker-compose down
	docker rmi -f better-budget-api

destroy-frontend:
	docker-compose down
	docker rmi -f better-budget-frontend