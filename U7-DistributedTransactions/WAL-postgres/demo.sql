-- WAL Log Demonstration Script
-- This script generates various types of WAL records for analysis
-- # by my guide with cursor

-- Transaction 0: Drop table if it exists
BEGIN;
DROP TABLE IF EXISTS oneshot_test;
COMMIT;

-- Transaction 1: Table creation and initial data
BEGIN;
CREATE TABLE oneshot_test (id SERIAL PRIMARY KEY, name TEXT, amount DECIMAL(10,2), created_at TIMESTAMP DEFAULT NOW());
CREATE INDEX idx_name ON oneshot_test(name);
INSERT INTO oneshot_test (name, amount) VALUES ('SAC', 100.50), ('SD', 200.75), ('WAL', 300.25);
COMMIT;

-- Transaction 2: Updates and modifications
BEGIN;
UPDATE oneshot_test SET name = 'SD_UPDATED', amount = 250.00 WHERE id = 2;
UPDATE oneshot_test SET amount = amount * 1.1 WHERE name LIKE 'S%';
COMMIT;

-- Transaction 3: Deletions and more inserts
BEGIN;
DELETE FROM oneshot_test WHERE id = 3;
INSERT INTO oneshot_test (name, amount) VALUES ('NEW_RECORD', 500.00), ('ANOTHER_ONE', 750.50);
COMMIT;

-- Transaction 4: Large batch operations (generates more WAL)
BEGIN;
INSERT INTO oneshot_test (name, amount) 
SELECT 'BATCH_' || i, (i * 10.5)::DECIMAL(10,2) 
FROM generate_series(1, 50) AS i;
COMMIT;

-- Transaction 5: Complex operations
BEGIN;
CREATE TABLE related_table (id SERIAL PRIMARY KEY, test_id INTEGER REFERENCES oneshot_test(id), description TEXT);
INSERT INTO related_table (test_id, description) 
SELECT id, 'Description for ' || name FROM oneshot_test WHERE amount > 100;
UPDATE oneshot_test SET amount = amount + 50 WHERE id IN (SELECT test_id FROM related_table);
COMMIT;

-- Transaction 6: Rollback scenario (WAL records but no commit)
BEGIN;
INSERT INTO oneshot_test (name, amount) VALUES ('ROLLBACK_TEST', 999.99);
UPDATE oneshot_test SET amount = 0 WHERE name = 'ROLLBACK_TEST';
-- This will be rolled back, but WAL records are still generated
ROLLBACK;

-- Force checkpoint to flush WAL
CHECKPOINT;

-- Transaction 7: Final operations
BEGIN;
DELETE FROM oneshot_test WHERE name LIKE 'BATCH_%';
UPDATE oneshot_test SET created_at = NOW() WHERE created_at IS NULL;
COMMIT;

-- Final checkpoint
CHECKPOINT;