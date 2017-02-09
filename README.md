A Historical Course Catalog
=======

This website allows students and professors to view documentation from past classes and projects and through time. It is also a convenient standard submission platform for class project documentation, and a tool for students to draw inspiration from each others' work.

##Current State
We've designed a relational database structure to store information about students, classes, and projects. 

**Insert database diagram**

We also built a rudimentary interface for students to log in and view their classes and projects, and to create new project documentation.

**Screenshots**

##Architecture
The code is broken into modules that interact through functional interfaces. The website is run by a Flask database stored in `server.py`. The server makes queries and stores information in the database through the `retrieveData` and `storeData` modules, which are heavily specialized for our particular application and database. Finally, the server renders the webpages defined in `/templates` using Jinja logic and Skeleton.css styles.

**Potentially diagrams**

##Future Work
Now that the database structure has been established, there are many potential additional functionalities for this project.

###User Login Process
(Completely un-implemented as of the end of MP1)

We would like this tool to integrate with existing institutional portals/web resources such that users can access it through familiar institutional sites and log in using their existing institutional credentials. 

###User Interactions by User Type
Primary users of this tool in its current form fall into two groups: students and professors. 
####Students 
(Somewhat implemented as of the end of MP1)

When students log in, they see the student dashboard. In its most basic form, this consists of a list of their current classes (potentially pulled from the institution's data given their credentials). They should also be able to navigate to classes from previous semesters to see their documentation of those projects. Upon selecting a class, the student is presented with a list of that class's projects. Upon selecting a project, the student either submits their documentation or is able to view the documentation they have submitted. For now, students are only able to see their own documentation for current classes. If a student is viewing documentation for a past class, it would be nice if they could see other students' project documentation as well. 
Classes should be labeled in the user's view with their course title and semester (ex. SP'17). 

####Professors
(Completely un-implemented as of the end of MP1)

When professors log in, they see the professor dashboard. In its most basic form, this consists of links to the classes they are teaching. Professors might also like to be able to see the projects in classes they are not currently teaching, so their dashboard may allow them to navigate to any class in the course catalog to view its data.
If they are...

1.Currently teaching a class, they can use this site to collect students' documentation of projects. Some interactions might include entering course project names so that students' documentation can be submitted under a consistent project name, browsing student documentation with a selection of sorting options, and perhaps responding to that documentation in some way.

2.Going to teach a class they haven't taught before, they can use this site to look back through the documentation of previous iterations of the class and gain understanding of its execution. 

###Architeture and Software Goodness
It would be nice if there were any security measures at all implemented, and some checks and robustness would be of great benefit. "This thing is still a baby, please don't be mean to it" is so far our only security measure. Pretty insufficient.

##Running The Code
Access the website by running`server.py` and navigating to 127.0.0.1:5000. Dependencies are [Sqlite3](https://www.sqlite.org/), [Flask](http://flask.pocoo.org), and [Skeleton](http://getskeleton.com/).
