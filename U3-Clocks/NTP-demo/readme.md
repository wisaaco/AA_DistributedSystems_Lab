# Steps

docker-compose up

docker exec -it ntp-client bash

chronyc sources -v

chronyc sourcestats -v

date

date --set="1980-10-12 10:05:59"

chronyd -q 'server 172.20.0.10 iburst'

date

