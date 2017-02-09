A Historical Course Catalog
=======

This website allows students and professors to view past classes and projects and track change through time. It is also a convenient standard submission platform for class projects, and a tool for students to draw inspiration from each others' work.

##Current State
We've designed a relational database structure to store information about students, classes, and projects.

**Insert database diagram**

We also built a rudimentary interface for students to log in and view their classes and projects, and to create new project documentation.

**Screenshots**

##Architecture
The code is broken into modules that interact through functional interfaces. The website is run by a Flask database stored in `server.py`. The server makes queries and stores information in the database through the `retrieveData` and `storeData` modules, which are heavily specialized for our particular application and database. Finally, the server renders the webpages defined found in `/templates` using Jinja logic and Skeleton.css styles.

**Potentially diagrams**

##Future Work

##Running The Code
Access the website by running`server.py` and navigating to 127.0.0.1:5000. Dependencies are [Sqlite3](https://www.sqlite.org/), [Flask](http://flask.pocoo.org), and [Skeleton](http://getskeleton.com/).
