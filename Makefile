build:
	docker-compose up

destroy:
	docker-compose down
	docker rmi -f better-budget-app