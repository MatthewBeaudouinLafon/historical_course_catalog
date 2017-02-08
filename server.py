import os, atexit

import pandas as pd
from flask import Flask, redirect, render_template, request, url_for, g

import retrieveData as retrieve
import storeData as store

import sqlite3

sqlite_file = "data.sqlite"

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
    return redirect('/user='+username)

@app.route('/new_user')
def new_user_page():	
    return render_template('new_user.html')

@app.route('/new_user', methods=['POST'])
def new_user():	
	c = get_db().cursor()
	name = request.form['name']
	username = request.form['username']
	store.new_student(c, name, username)
	return redirect("/login")

@app.route('/user=<username>')
def your_classes(username):	
    return render_template('student_dashboard.html', username=username)

@app.route('/user=<username>/class=<class_name>')
def show_single_class(username, class_name):
	c=get_db().cursor()
	student_id=retrieve.find_student_id(c, username)
	name=retrieve.find_student_name(c, student_id)
	return render_template('class_dashboard.html', username=username, class_name=class_name, name=name)

# @app.route('/project_page')
# def login():	
#     return render_template('project_page.html')

# @app.route('/input_form')
# def login():	
#     return render_template('input_form.html')

# @app.route('/area/<course_area>')
# def area_page(course_area):
#     return render_template('course_area.html', courses=courses[courses.course_area == course_area].iterrows())

# def end_func(conn):
# 	conn.commit()
# 	conn.close()

if __name__ == '__main__':

	atexit.register(close_connection)
	app.run(debug=True, threaded=True)
