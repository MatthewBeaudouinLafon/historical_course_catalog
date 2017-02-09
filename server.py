import os, atexit

import pandas as pd
from flask import Flask, redirect, render_template, request, url_for, g

import retrieveData as retrieve
import storeData as store

import sqlite3

#sqlite_file = "data.sqlite"
sqlite_file = "test_data.sqlite"

# conn = sqlite3.connect(sqlite_file)
# c = conn.cursor()

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(sqlite_file)
	return db

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv

app = Flask(__name__)


@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.commit()
		db.close()

@app.route('/health')
def health():
    return 'ok'

@app.route('/')
def home_redir():
	return redirect("/login")

@app.route('/login')
def login_page():	
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():	
	username = request.form['username']
	c = get_db().cursor()
	student_id = retrieve.find_student_id(c, username)
	return redirect('/user='+str(student_id))

@app.route('/new_user')
def new_user_page():	
	return render_template('new_user.html')

@app.route('/new_user', methods=['POST'])
def new_user():	
	c = get_db().cursor()
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	username = request.form['username']
	student_id = store.new_student(c, first_name, last_name, username)
	return redirect("/user="+str(student_id))

@app.route('/user=<student_id>')
def your_classes(student_id):	
	c = get_db().cursor()
	name = retrieve.find_student_name(c, student_id)

	class_ids = retrieve.find_students_classes(c, student_id)
	class_names = [retrieve.find_class_name(c, class_id) for class_id in class_ids]
	classes = dict(zip(class_ids, class_names))			#Map ids to names
	print(classes)

	project_ids = retrieve.find_students_projects(c, student_id)
	project_names = [retrieve.find_project_title(c, project_id) for project_id in project_ids]
	projects = dict(zip(project_ids, project_names))	#Map ids to names
	print(projects)

	classes_projects = [(class_ids[i] if len(class_ids)>i else None, project_ids[i] if \
		len(project_ids)>i else None) for i in range(max(len(class_ids), len(project_ids)))]		#Create an iterable of classes and projcts
	print(classes_projects)
	return render_template('student_dashboard.html', student_id=student_id, name = name, classes_projects=classes_projects, \
		classes=classes, projects=projects)

@app.route('/user=<student_id>/class=<class_id>')
def show_single_class(student_id, class_id):
	c=get_db().cursor()
	project_ids=retrieve.find_students_class_projects(c, class_id, student_id)
	projects=[]
	for project_id in project_ids:
		project_name=retrieve.find_project_title(c, project_id)
		projects.append({'name':project_name, 'id':project_id})
	#project_names=[retrieve.find_project_title(c, project_id) for project_id in project_ids]
	class_name=retrieve.find_class_name(c, class_id)
	return render_template('class_dashboard.html', projects=projects, class_name=class_name, student_id=student_id)

@app.route('/user=<student_id>/class=<class_id>/project_form')
def new_project_page(student_id, class_id):
	return render_template('project_form.html')

@app.route('/user=<student_id>/class=<class_id>/project_form', methods=['POST'])
def new_project(student_id, class_id):
	c = get_db().cursor()

	title = request.form['title']
	students = request.form['students']
	description = request.form['description']
	link = request.form['link']

	student_ids = [student_id]
	for user in students.split(', '):
		student_ids.append(retrieve.find_student_id(c, user))

	project_id = store.new_project(c, class_id, title, description, link, student_ids)
	return redirect("/user=<student_id>/class=<class_id>/project="+str(project_id))

@app.route('/user=<student_id>/class=<class_id>/project=<project_id>')
def show_project(student_id, class_id, project_id):
	c = get_db().cursor()
	title = retrieve.find_project_title(c, project_id)
	descr = retrieve.find_project_descr(c, project_id)
	link = retrieve.find_project_link(c, project_id)
	class_name = retrieve.find_class_name(c, retrieve.find_project_class(c, project_id))
	student_ids = retrieve.find_project_students(c, project_id)
	student_names = [retrieve.find_student_name(c, student_id) for student_id in student_ids]
	return render_template('project_dashboard.html', title=title, descr=descr, link=link, class_name=class_name, student_names=student_names, project_id=project_id)

if __name__ == '__main__':

	atexit.register(close_connection)
	app.run(debug=True, threaded=True)
