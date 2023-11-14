CREATE TABLE IF NOT EXISTS test_database.items (
    item_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    price FLOAT NOT NULL,
    name VARCHAR(32) NOT NULL
);

INSERT INTO test_database.items VALUES (NULL, 100, 'kek1');
INSERT INTO test_database.items VALUES (NULL, 200, 'kek2');
INSERT INTO test_database.items VALUES (NULL, 300, 'kek3');
