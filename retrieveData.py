"""
This is a module with functions that take a database and a some kind of search terms,
and return data in some form. Basically, strip unnecessary code out of the main server section.
We should probably condense these functions to make them more general-purpose, and maybe create a class wrapper
""" 
import sqlite3

def find_student_id(c, user):
	c.execute("SELECT student_id FROM student WHERE user=(?)", (user, ))
	the_id = c.fetchone()
	if the_id:
		return the_id[0]
	else:
		raise ValueError

def find_students_in_class(c, class_id):		#Return a list of names of students in a class with a certain class_id
	c.execute("SELECT student_id FROM class_student WHERE class_id=(?)", (class_id, ))
	student_ids=tuple([thing[0] for thing in c.fetchall()])		#create a tuple of all student ids in the class
	return student_ids
	# c.execute("SELECT (name) FROM student WHERE student_id in (" + ",".join("?"*len(student_ids)) + ")", student_ids)     #This is not elegant, but I couldn't get executemany to work
	# return c.fetchall()

def find_students_classes(c, student_id): 		#Return a list of the classes a student is in
	c.execute("SELECT class_id FROM class_student WHERE student_id=(?)", (student_id, ))
	class_ids=tuple([thing[0] for thing in c.fetchall()])		#create a tuple of all the class_ids a student has
	return class_ids
	# c.execute("SELECT (name) FROM class WHERE class_id in (" + ",".join("?"*len(class_ids)) + ")", class_ids)     #This is not elegant, but I couldn't get executemany to work
	# return c.fetchall()

def find_students_projects(c, student_id):		#Return a list of all a student's projects
	c.execute("SELECT project_id FROM student_project WHERE student_id=(?)", (student_id, ))
	project_ids=tuple([thing[0] for thing in c.fetchall()])
	return project_ids

def find_students_class_projects(c, class_id, student_id):
	c.execute("SELECT project.project_id FROM project, student_project WHERE project.project_id == student_project.project_id AND student_project.student_id=(?) and project.class_id=(?)", (student_id, class_id))
	project_ids=tuple([thing[0] for thing in c.fetchall()])
	return project_ids
	# c.execute("SELECT title FROM project WHERE project_id in (" + ",".join("?"*len(project_ids)) + ")", project_ids)
	# return c.fetchall()

def find_project_students(c, project_id):		#Return a list of students on a project
	c.execute("SELECT student_id FROM student_project WHERE project_id=(?)", (project_id, ))
	student_ids=tuple([thing[0] for thing in c.fetchall()])
	return student_ids

def find_classes_projects(c, class_id):			#Return a list of all projects in a class
	c.execute("SELECT title FROM project WHERE class_id=(?)", (class_id, ))
	return c.fetchall()

def find_class_name(c, class_id):				#Tell you the name of a class based on id
	c.execute("SELECT name FROM class WHERE class_id=(?)", (class_id, ))
	return c.fetchone()[0]

def find_student_name(c, student_id):			#Tell you the name of a student based on id
	print("Student ID: " + str(student_id))
	c.execute("SELECT first_name, last_name FROM student WHERE student_id=(?)", (student_id, ))
	full_name = c.fetchone()
	return (" ".join(full_name))

def find_project_title(c, project_id):			#Tell you the title of a project based on id
	c.execute("SELECT title FROM project WHERE project_id=(?)", (project_id, ))
	return c.fetchone()[0]

def find_project_descr(c, project_id):			#Gives you the description of a project based on id
	c.execute("SELECT description FROM project WHERE project_id=(?)", (project_id, ))
	return c.fetchone()[0]

def find_project_link(c, project_id):			#Gives you the link of a project based on id
	c.execute("SELECT link FROM project WHERE project_id=(?)", (project_id, ))
	return c.fetchone()[0]

def find_project_class(c, project_id):			#Gives you the link of a project based on id
	c.execute("SELECT class_id FROM project WHERE project_id=(?)", (project_id, ))
	return c.fetchone()[0]