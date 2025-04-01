start:
	docker build -t scheduling-service-app:latest scheduling-service/ --no-cache
	docker build -t ordering-service-app:latest ordering-service/ --no-cache
	kubectl apply -f ./job-storage-service/
	kubectl apply -f ./log-storage-service/
	kubectl apply -f ./queue-service/
	kubectl apply -f ./scheduling-service/
	kubectl apply -f ./ordering-service/

down:
	kubectl delete services app
	kubectl delete services ordering-app
	kubectl delete services postgres
	kubectl delete services mongodb
	kubectl delete services rabbitmq
	kubectl delete deployments app
	kubectl delete deployments ordering-app
	kubectl delete deployments postgres
	kubectl delete deployments mongodb
	kubectl delete deployments rabbitmq
	kubectl delete pod -l app=app
	kubectl delete pod -l app=ordering-app
	kubectl delete pod -l app=postgres
	kubectl delete pod -l app=mongodb
	kubectl delete pod -l app=rabbitmq
