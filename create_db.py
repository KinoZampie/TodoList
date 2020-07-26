import sqlite3

todo_data = sqlite3.connect("assignments_tracker.db")

c = todo_data.cursor()

# Create Users Table
'''
c.execute("""CREATE TABLE "users" (
	"id"	INTEGER NOT NULL,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);""")
'''

# Create Tasks Table
'''
c.execute("""CREATE TABLE "tasks" (
	"id"	INTEGER NOT NULL,
	"task_user"	TEXT NOT NULL,
	"task_description"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);""")
'''

todo_data.commit()

todo_data.close()