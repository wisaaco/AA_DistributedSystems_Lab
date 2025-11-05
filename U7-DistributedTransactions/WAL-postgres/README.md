# Viewing the PostrgreSQL WAL

## How to use the project

Steps:

```bash
docker-compose up -d
docker exec -it pg-wal-demo psql -U postgres

SHOW data_directory;
SHOW wal_level;
SHOW wal_log_hints;
SHOW archive_mode;
SHOW log_directory;

```

Default values of those SHOWs:

```text
postgres=# SHOW wal_level;
 wal_level 
-----------
 replica
(1 row)

postgres=# SHOW wal_log_hints;
 wal_log_hints 
---------------
 off
(1 row)

postgres=# SHOW archive_mode;
 archive_mode 
--------------
 off
(1 row)

postgres=# SHOW log_directory;
 log_directory 
---------------
 log
(1 row)

postgres=# SHOW data_directory;
      data_directory      
--------------------------
 /var/lib/postgresql/data
(1 row)

```

Where the WAL logs are recorded (). Each one has 16 MB by default in a binary format.

```` bash
docker exec -it pg-wal-demo ls -li /var/lib/postgresql/data/pg_wal/ -li
docker exec -it pg-wal-demo pg_waldump /var/lib/postgresql/data/pg_wal/000000010000000000000001 | tail -n 20

total 16384
99475943 -rw------- 1 postgres postgres 16777216 Oct 24 07:24 000000010000000000000001
99475914 drwx------ 2 postgres postgres       64 Oct 24 07:22 archive_status

```


## PG WAL structure

On two terminals

```bash
#1
./run_demo.sh

#2
docker exec -it pg-wal-demo bash
cd /var/lib/postgresql/data/pg_wal/
pg_waldump 000000010000000000000001
```
or ```docker exec -it pg-wal-demo pg_waldump 000000010000000000000001 > wal_dump.txt````


An example:
```bash
rmgr: Heap        len (rec/tot):    238/   238, tx:        761, lsn: 0/0162CCF0, prev 0/0162CCB0, desc: INSERT off: 12, flags: 0x00, blkref #0: rel 1663/5/2619 blk 18
rmgr: Btree       len (rec/tot):     64/    64, tx:        761, lsn: 0/0162CDE0, prev 0/0162CCF0, desc: INSERT_LEAF off: 47, blkref #0: rel 1663/5/2696 blk 2
rmgr: Transaction len (rec/tot):    114/   114, tx:        761, lsn: 0/0162CE20, prev 0/0162CDE0, desc: COMMIT 2025-10-24 07:40:03.048826 UTC; inval msgs: catcache 63 catcache 63 catcache 63 catcache 63
rmgr: Standby     len (rec/tot):     50/    50, tx:          0, lsn: 0/0162CE98, prev 0/0162CE20, desc: RUNNING_XACTS nextXid 762 latestCompletedXid 761 oldestRunningXid 762
```

- Heap Records (Data Changes):
    rmgr: Heap = This is a data modification (INSERT/UPDATE/DELETE)
    tx: 761 = Transaction ID 761
    lsn: 0/0162B5D0 = Log Sequence Number (unique identifier) (show the order of operations!!)
    desc: INSERT off: 9 = INSERT operation at offset 9 in the page
    rel 1663/5/2619 = Relation (table) identifier
    blk 18 = Block number 18
    FPW = Full Page Write (entire page was written to WAL!!)

- Btree Records (Index Changes)
    rmgr: Btree = Index operation
    desc: INSERT_LEAF = Inserting into a leaf node of the B-tree index
    rel 1663/5/2696 = Index relation identifier

- Transaction Records (boundaries are clearly marked!!)
    rmgr: Transaction = Transaction control operation
    desc: COMMIT = Transaction 761 was committed
    inval msgs = Cache invalidation messages

-  Standby Records
    rmgr: Standby = Standby/replication information
    RUNNING_XACTS = Running transactions snapshot
    nextXid 762 = Next transaction ID will be 762




# Activity: Can you identify in the WAL the transactions from @demo.sh file?

A tip code: *Force another WAL file*

```bash
docker exec -it pg-wal-demo psql -U postgres -c "
SELECT pg_switch_wal();
CHECKPOINT;
"

docker exec -it pg-wal-demo ls -la /var/lib/postgresql/data/pg_wal/
```


#### Clean this project
- Remove the ./pgdata
- Remove container and images

´´´bash
docker-compose down
rm -rf ./pgdata
docker rmi postgres:16
```