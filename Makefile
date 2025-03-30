start:
	docker build -t scheduling-service-app:latest scheduling-service/ --no-cache
	kubectl apply -f ./job-storage-service/
	kubectl apply -f ./queue-service/
	kubectl apply -f ./scheduling-service/

down:
	kubectl delete services app
	kubectl delete services postgres
	kubectl delete services rabbitmq
	kubectl delete deployments app
	kubectl delete deployments postgres
	kubectl delete deployments rabbitmq
	kubectl delete pod -l app=app
	kubectl delete pod -l postgres=postgres
	kubectl delete pod -l rabbitmq=rabbitmq


