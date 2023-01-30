#sudo docker container run -it -p 4243:4243 --entrypoint /bin/bash -t db
sudo docker build -t db -f postgres_firebird.docker .
sudo docker container run -it -p 4243:4243 -t db
