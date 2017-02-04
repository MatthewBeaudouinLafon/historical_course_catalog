"""
This is a module with functions that take a database and a some kind of search terms,
and return data in some form. Basically, strip unnecessary code out of the main server section.
""" 
import sqlite3

def find_students_in_class(c, class_id):		#Return a list of names of students in a class with a certain class_id
	c.execute("select student_id from class_student where class_id=(?)", (class_id, ))
	student_ids=tuple([thing[0] for thing in c.fetchall()])
	c.execute("SELECT (name) FROM student WHERE student_id in (" + ",".join("?"*len(student_ids)) + ")", student_ids)     #This is not elegant, but I couldn't get executemany to work
	return c.fetchall()