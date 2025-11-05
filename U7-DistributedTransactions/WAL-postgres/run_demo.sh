#! /bin/bash

# 
docker cp ./demo.sql pg-wal-demo:/demo.sql  
docker exec -it pg-wal-demo psql -U postgres -d postgres -f /demo.sql