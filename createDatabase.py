# This script sets up the SQLite database
import sqlite3

sqlite_file = "data.sqlite"

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Create tables
c.execute("""CREATE TABLE IF NOT EXISTS student(
	student_id	INTEGER			PRIMARY KEY 	AUTOINCREMENT,
	name	TEXT			NOT NULL,
	user	TEXT			NOT NULL
	)""")

c.execute('CREATE UNIQUE INDEX usernames ON student (user)')		#Make it so you can look up students quickly by username

c.execute("""CREATE TABLE IF NOT EXISTS class(
	class_id 	INTEGER			PRIMARY KEY 	AUTOINCREMENT,
	name		TEXT			NOT NULL
	)""")

c.execute("""CREATE TABLE IF NOT EXISTS project(
	project_id	INTEGER			PRIMARY KEY 	AUTOINCREMENT,
	title		TEXT			NOT NULL,
	class_id    INTEGER			NOT NULL
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

conn.commit()
conn.close()