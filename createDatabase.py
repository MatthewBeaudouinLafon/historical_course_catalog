# This script sets up the SQLite database
import sqlite3

# sqlite_file = "data.sqlite"
sqlite_file = "test_data.sqlite"

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

### Create tables

# student
c.execute("""CREATE TABLE IF NOT EXISTS student(
	student_id	INTEGER			PRIMARY KEY 	AUTOINCREMENT,
	first_name	TEXT			NOT NULL,
	last_name	TEXT			NOT NULL,
	user		TEXT			NOT NULL
	)""")

# Make it so you can look up students quickly by username
c.execute('CREATE UNIQUE INDEX IF NOT EXISTS usernames ON student (user)')		

# class
c.execute("""CREATE TABLE IF NOT EXISTS class(
	class_id 	INTEGER			PRIMARY KEY 	AUTOINCREMENT,
	name		TEXT			NOT NULL
	)""")

# project
c.execute("""CREATE TABLE IF NOT EXISTS project(
	project_id	INTEGER			PRIMARY KEY 	AUTOINCREMENT,
	class_id    INTEGER			NOT NULL,
	title		TEXT			NOT NULL,
	description	TEXT			NOT NULL,
	link		TEXT
	)""")

# JOIN class student
c.execute("""CREATE TABLE IF NOT EXISTS class_student(
	class_id	INTEGER				NOT NULL,
	student_id	INTEGER				NOT NULL
	)""")

# JOIN student project
c.execute("""CREATE TABLE IF NOT EXISTS student_project(
	student_id	INTEGER				NOT NULL,
	project_id	INTEGER				NOT NULL
	)""")

print("Created tables")


### Populate table with tests

# Add a bunch of students
test_students = [('John', 'Doe', 'jdoe'),
				 ('Grace', 'Hopper', 'ghopper'),
				 ('Alan', 'Turing', 'aturing'),
				]

c.executemany("INSERT OR REPLACE INTO student (first_name, last_name, user) VALUES (?,?,?)", test_students)

# Add some classes
test_classes = [('AHSE: Art of Being a Test',),
				('ENGR: Making an impact on Computing',)]

c.executemany("INSERT OR REPLACE INTO class (name) VALUES (?)", test_classes)

# Add students to classes
#	Get students
testers = []
for person in [('jdoe',), ('ghopper',), ('aturing',)]:
	c.execute("SELECT student_id FROM student WHERE user=?", person)
	testers.append(c.fetchone())

computer_people = []
for person in [('ghopper',), ('aturing',)]:
	c.execute("SELECT student_id FROM student WHERE user=?", person)
	computer_people.append(c.fetchone())

#	Get class
c.execute("SELECT class_id FROM class WHERE name=?", ('AHSE: Art of Being a Test',))
class_test = c.fetchone()

c.execute("SELECT class_id FROM class WHERE name=?", ('ENGR: Making an impact on Computing',))
class_computer = c.fetchone()

#	Add students to classes
for tester in testers:
	c.execute("INSERT OR REPLACE INTO class_student (class_id, student_id) VALUES (?,?)", (class_test[0], tester[0]))

for computer_person in computer_people:
	c.execute("INSERT OR REPLACE INTO class_student (class_id, student_id) VALUES (?,?)", (class_computer[0], computer_person[0]))


# Add projects
#	Create projects
c.execute("INSERT OR REPLACE INTO project (class_id, title, description, link) VALUES (?,?,?,?)", (class_test[0], "The Test Project", "Lorem ipsum", "https://www.test.com/"))
project_test = c.lastrowid

c.execute("INSERT OR REPLACE INTO project (class_id, title, description, link) VALUES (?,?,?,?)", (class_computer[0], "Enigma", "Winning WWII", "https://en.wikipedia.org/wiki/Enigma_machine"))
project_enigma = c.lastrowid

#	Join students and classes
c.execute("SELECT student_id FROM student WHERE user=?", ('aturing',))
turing = c.fetchone()

for tester in testers:
	c.execute("INSERT OR REPLACE INTO student_project (student_id, project_id) VALUES (?,?)", (tester[0], project_test))

c.execute("INSERT OR REPLACE INTO student_project (student_id, project_id) VALUES (?,?)", (turing[0], project_enigma))

print("Populated Database")

conn.commit()
conn.close()
