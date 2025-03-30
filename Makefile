start:
	docker build -t scheduling-service-app:latest scheduling-service/
	kubectl apply -f ./job-storage-service/
	kubectl apply -f ./queue-service/
	kubectl apply -f ./scheduling-service/


