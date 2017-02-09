"""
This is another module that has functions which take a database and some information, and store that information in the
database. We might want to add this one to retrieveData.py and create a single class that inherits from cursor or something
The login is structured so a username and password correspond to a student_id. So, unless it's a new student, you know the 
student_id
"""
from __future__ import print_function
import sqlite3
import sys

def new_student(c, first_name, last_name, user, class_ids=[]):			#Create a new student, put them into certain classes
	try:
		print("Adding {} as {}".format(first_name+" "+last_name, user), file=sys.stderr)
		c.execute("INSERT INTO student (first_name, last_name, user) VALUES (?, ?, ?)", (first_name, last_name, user))
	except sqlite3.IntegrityError:
		return "Username already in use"			#Needs some work
	student_id = c.lastrowid
	for class_id in class_ids:
		add_students_class(c, class_id, [student_id])
	return student_id

def new_class(c, name, student_ids=[]):			#Create a new class with certain students
	c.execute("INSERT INTO class (name) VALUES (?)", (name, ))
	class_id = c.lastrowid
	add_students_class(c, class_id, student_ids)
	return class_id

def new_project(c, class_id, title, description, link, student_ids=[]):		#Create a new project in a class w/students
	c.execute("INSERT INTO project (title, class_id, description, link) VALUES (?, ?, ?, ?)", (title, class_id, description, link))
	project_id = c.lastrowid
	for student_id in student_ids:
		c.execute("INSERT INTO student_project (student_id, project_id) VALUES (?, ?)", (student_id, project_id))
	return project_id

def add_students_class(c, class_id, student_ids):		#Add students to an existing class; student_ids must be a list
	print(student_ids)
	for student_id in student_ids:
		print(type(class_id))
		c.execute("SELECT * FROM class_student WHERE (class_id)=? AND (student_id)=?", (class_id, student_id))
		if not c.fetchone():			#Check that this student isn't already in this class
			c.execute("INSERT INTO class_student (class_id, student_id) VALUES (?, ?)", (class_id, student_id))

def add_students_project(c, project_id, student_ids):	#Add students to a project team; student_ids must be a list
	for student_id in student_ids:
		c.execute("SELECT * FROM class_student WHERE (project_id)=? AND (student_id)=?", (project_id, student_id))
		if not c.fetchone():			#Check that this student isn't already in this class
			c.execute("INSERT INTO student_project (project_id, student_id) VALUES (?, ?)", (project_id, student_id))