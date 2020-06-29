-- Step 1:
CREATE SCHEMA assignments_tracker_db;

-- Step 2:
USE assignments_tracker_db;

-- Step 3:
CREATE TABLE users(
id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(30) NOT NULL UNIQUE,
password VARCHAR(60) NOT NULL
);

-- Step 4:
CREATE TABLE tasks(
id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
task_user VARCHAR(30) NOT NULL,
task_description VARCHAR(300) NOT NULL
);

