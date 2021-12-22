sudo docker-compose -f docker-compose.yml up -d --build database

DATABASE_IP=$(sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' database) 

echo $DATABASE_IP

DATABASE_IP=$DATABASE_IP sudo docker-compose -f docker-compose.yml up -d --build create_database