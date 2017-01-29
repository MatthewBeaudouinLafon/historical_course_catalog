# This script sets up the SQLite database
import sqlite3

sqlite_file = "data.sqlite"

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Create tables
c.execute("""CREATE TABLE IF NOT EXISTS student(
	student_id	INTEGER			PRIMARY KEY 	AUTOINCREMENT,
	first_name	TEXT			NOT NULL,
	last_name	TEXT			NOT NULL
	)""")

c.execute("""CREATE TABLE IF NOT EXISTS class(
	class_id 	INTEGER			PRIMARY KEY 	AUTOINCREMENT,
	name		TEXT			NOT NULL,
	olin_id		TEXT			NOT NULL,
	semester	TEXT			NOT NULL
	)""")

c.execute("""CREATE TABLE IF NOT EXISTS project(
	project_id	INTEGER			PRIMARY KEY 	AUTOINCREMENT,
	title		TEXT			NOT NULL,
	semester	TEXT			NOT NULL,
	start_date	TEXT,
	pdf_path	TEXT
	)""")

c.execute("""CREATE TABLE IF NOT EXISTS class_student(
	class_id	INTEGER				NOT NULL,
	student_id	INTEGER				NOT NULL
	)""")

c.execute("""CREATE TABLE IF NOT EXISTS student_project(
	student_id	INTEGER				NOT NULL,
	project_id	INTEGER				NOT NULL
	)""")

print("Created tables")

# Create dummy variables
c.execute("INSERT INTO student (first_name, last_name) VALUES (?, ?)", ('JOHN', 'DOE'))
student_id = c.lastrowid

c.execute("INSERT INTO class (name, olin_id, semester) VALUES (?, ?, ?)", ('Hacking the Library', 'ENGR3599A-01', 'SP2017'))
class_id = c.lastrowid

c.execute("INSERT INTO class_student (class_id, student_id) VALUES (?,?)", (class_id, student_id))

print("Added dummy variable")

conn.commit()
conn.close()