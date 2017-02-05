"""
This is another module that has functions which take a database and some information, and store that information in the
database. We might want to add this one to retrieveData.py and create a single class that inherits from cursor or something
The login is structured so a username and password correspond to a student_id. So, unless it's a new student, you know the 
student_id
"""
import sqlite3

def new_student(c, name, class_ids=[]):			#Create a new student, put them into certain classes
	c.execute("INSERT INTO student (name) VALUES (?)", (name, ))
	student_id = c.lastrowid
	for class_id in class_ids:
		c.execute("INSERT INTO class_student (class_id, student_id) VALUES (?, ?)", (class_id, student_id))
	return student_id

def new_class(c, name, student_ids=[]):			#Create a new class with certain students
	c.execute("INSERT INTO class (name) VALUES (?)", (name, ))
	class_id = c.lastrowid
	for student_id in student_ids:
		c.execute("INSERT INTO class_student (class_id, student_id) VALUES (?, ?)", (class_id, student_id))
	return class_id

def new_project(c, class_id, student_ids=[], project_title="Alice in Wonderland"):		#Create a new project in a class w/students
	c.execute("INSERT INTO project (title, class_id) VALUES (?, ?)", (project_title, class_id))
	project_id = c.lastrowid
	for student_id in student_ids:
		c.execute("INSERT INTO student_project (student_id, project_id) VALUES (?, ?)", (student_id, project_id))
	return project_id

def add_students_class(c, class_id, student_ids):		#Add students to an existing class; student_ids must be a list
	for student_id in student_ids:
		c.execute("SELECT * FROM class_student WHERE (class_id, student_id) = (?, ?)", (class_id, student_id))
		if not c.fetchone():			#Check that this student isn't already in this class
			c.execute("INSERT INTO class_student (class_id, student_id) VALUES (?, ?)", (class_id, student_id))

def add_students_project(c, project_id, student_ids):	#Add students to a project team; student_ids must be a list
	for student_id in student_ids:
		c.execute("SELECT * FROM student_project WHERE (student_id, project_id) = (?, ?)", (student_id, project_id))
		if not c.fetchone():			#Check that this student isn't already in this class
			c.execute("INSERT INTO student_project (student_id, project_id) VALUES (?, ?)", (student_id, project_id))