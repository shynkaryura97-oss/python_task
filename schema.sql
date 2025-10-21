-- schema.sql
CREATE TABLE IF NOT EXISTS rooms (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    id INT PRIMARY KEY,
    birthday DATETIME NOT NULL,
    sex VARCHAR(1) NOT NULL,
    name VARCHAR(255) NOT NULL,
    room_id INT NOT NULL,
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);
