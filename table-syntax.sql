-- CREATING DATABASE
CREATE DATABASE flask_db;

-- creating database with condition
CREATE DATABASE IF NOT EXISTS flask_db;

-- tables
CREATE TABLE student (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    course VARCHAR(50)
)

-- default INT is 11, max that can be specified 255
CREATE TABLE student (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    phone VARCHAR(15),
    salary INT
)

-- DELETE TABLE
DROP TABLE table_name
-- EMPTY CONTENT OF TABLE
TRUNCATE TABLE table_name
-- alter content of a table
ALTER TABLE table_name CHANGE column_name column_new_name data_type new_data_type
-- to rename a table name
ALTER TABLE teacher RENAME teachers


-- USING C.R.U.D - CREATE, READ, UPDATE AND DELETE

-- CREATE - TO CREATE WE USE INSERT
-- ID, NAME, COURSE
-- INSERTING SINGLE RECORDS IN THE TABLE
INSERT INTO student (name, course) VALUES ('JACE ALEXANDER', 'SQL');
-- INSERTING MULTIPLE RECORDS IN THE TABLE
INSERT INTO student (name, course) VALUES ('JOHN CHAMPION', 'PYTHON'), ('JIM BEGLIN', 'JAVA'), ('PAUL WALSH', 'HTML');

-- READ - TO READ WE USE SELECT
-- Syntax -> SELECT column_name FROM table_name
select name from student;
-- selecting multiple fields/columns
select name, course from student;
-- to select all fields/columns
select * from student;
-- conditional selection
select * from student where id < 3;
-- select where course = sql
select * from student where course = 'SQL';

-- UPDATE - WE USE UPDATE
-- SYNTAX -> UPDATE table_name SET column_name = 'new_value', column_name = 'new_value' where column_name = 'value';
update student set name = 'Mark Smith', course = 'PHP' where name = 'Jace Alexander';

-- DELETE - WE USE DELETE
-- SYNTAX -> DELETE FROM table_name WHERE column_name = value and column_name = value;
delete from student where id = 1 and id = 3;




