import sqlite3
import retrieveData as retrieve
import storeData as store

sqlite_file = "data.sqlite"

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

print(store.new_student(c, "Mike"))

thing = retrieve.find_students_in_class(c, 1)
print("Students in " + retrieve.find_class_name(c, 1)[0] + ": " + str(thing))

thing = retrieve.find_students_classes(c, 4)
print(thing)

thing = retrieve.find_students_projects(c, 3)
print(thing)

conn.close()