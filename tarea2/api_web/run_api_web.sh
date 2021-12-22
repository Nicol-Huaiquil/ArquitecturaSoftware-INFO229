DATABASE_IP = $(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' database)
DATABASE_IP=$DATABASE_IP sudo docker-compose up --build -d
#DATABASE_IP = "172.17.0.2" sudo docker-compose up --build -d