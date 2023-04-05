import sqlite3
import csv
import tabulate as tab
import itertools

backkey = "<"


def update():
	print("-Enter '" + backkey + "' to go back-")


# Inserting data from the csvs to the databases
def insertCSVs():
	with open("13 Databases data (1) - Classes.csv", "r") as file:
		for row in csv.reader(file):
			c.execute("""INSERT INTO Classes (ID,Name,YearLevel,TeacherID) 
						VALUES (?, ?, ?, ?);""", (row[0], row[1], row[2], row[3]))

	with open("13 Databases data (1) - Students.csv", "r") as file:
		for row in csv.reader(file):
			c.execute("""INSERT INTO Students (ID,first_name,last_name,YearLevel) 
						VALUES (?, ?, ?, ?);""", (row[0], row[1], row[2], row[3]))

	with open("13 Databases data (1) - Students and Classes.csv", "r") as file:
		for row in csv.reader(file):
			c.execute("""INSERT INTO StudentsAndClasses (StudentID,ClassID) 
						VALUES (?, ?);""", (row[0], row[1]))

	with open("13 Databases data (1) - Students with timetables.csv", "r") as file:
		for row in csv.reader(file):
			c.execute("""INSERT INTO StudentsWithTimetables (first_name,last_name,YearLevel,Subject1,Subject2,Subject3,Subject4,Subject5,Subject6) 
						VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

	with open("13 Databases data (1) - Teachers.csv", "r") as file:
		for row in csv.reader(file):
			c.execute("""INSERT INTO Teachers (ID,FirstName,LastName) 
						VALUES (?, ?, ?);""", (row[0], row[1], row[2]))


connect = sqlite3.connect('Database.db')
c = connect.cursor()

# This sets the thing
reset = True
if reset:
	c.execute("DROP TABLE IF EXISTS 'Classes';")
	c.execute("DROP TABLE IF EXISTS 'Students';")
	c.execute("DROP TABLE IF EXISTS 'StudentsAndClasses';")
	c.execute("DROP TABLE IF EXISTS 'StudentsWithTimetables';")
	c.execute("DROP TABLE IF EXISTS 'Teachers';")

	# Creating tables
	c.execute("""
	CREATE TABLE Classes (
		ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		Name TEXT NOT NULL,
		YearLevel INTEGER NOT NULL,
		TeacherID INTEGER NOT NULL,
		FOREIGN KEY (TeacherID) REFERENCES Teachers(ID)
	);
	""")
	c.execute("""
	CREATE TABLE Students (
		ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		first_name TEXT NOT NULL,
		last_name TEXT NOT NULL,
		YearLevel INTEGER NOT NULL
	);
	""")
	c.execute("""
	CREATE TABLE StudentsAndClasses (
		StudentID INTEGER NOT NULL,
		ClassID INTEGER NOT NULL,
		FOREIGN KEY (StudentID) REFERENCES Students(ID),
		FOREIGN KEY (ClassID) REFERENCES Classes(ID)
	);
	""")
	c.execute("""
	CREATE TABLE StudentsWithTimetables (
		StudentID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		first_name TEXT NOT NULL,
		last_name TEXT NOT NULL,
		YearLevel INTEGER NOT NULL,
		Subject1 TEXT NOT NULL,
		Subject2 TEXT NOT NULL,
		Subject3 TEXT NOT NULL,
		Subject4 TEXT NOT NULL,
		Subject5 TEXT NOT NULL,
		Subject6 TEXT NOT NULL,
		FOREIGN KEY (StudentID) REFERENCES Students(ID)
	);
	""")
	c.execute("""
	CREATE TABLE Teachers (
		ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		FirstName TEXT NOT NULL,
		LastName TEXT NOT NULL
	);
	""")
	insertCSVs()
	connect.commit()

c.execute("""SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';""")
tables = c.fetchall()


def main():
	while True:
		search()
	while True:
		action = input("hey do you want to search something (1) or add something (2): ")
		try:
			if int(action) == 1:
				search()
			elif int(action) == 2:
				add()
		except ValueError:
			pass


def search():
	# printing out available columns across all tables
	columnID = 0
	columnDict = {}
	for i, table in enumerate(tables):
		string = ""
		c.execute(f"PRAGMA table_info({table[0]});")
		for columnInfo in c.fetchall():
			columnID += 1
			string += f"{columnInfo[1]} ({columnID}), "
			columnDict[columnID] = f"{table[0]}.{columnInfo[1]}"
		print(f"{table[0]}: {string}")

	while True:
		try:
			selected = input("hey lets enter some specific columns you want to search stuff in, eg. 1,2,3: ")
			columns = [columnDict[int(i)] for i in selected.split(",")]
			print(', '.join(columns))
			selectedtables = [column.split('.', 1)[0] for column in columns]
			print(selectedtables)
			break
		except ValueError:
			pass
		except KeyError:
			pass
	joinings = ""
	if 'Students' in selectedtables and 'Classes' in selectedtables:
		joinings += """
		FROM (StudentsAndClasses)
		INNER JOIN Students ON Students.ID = StudentsAndClasses.StudentID
		INNER JOIN Classes ON Classes.ID = StudentsAndClasses.ClassID"""
	if 'Teachers' in selectedtables and 'Classes' in selectedtables:
		joinings += """
		FROM (Classes)
		INNER JOIN Teachers ON Teachers.ID = Classes.TeacherID"""

	orderings = "ORDER BY"
	for column in columns:
		orderings += f" {column} ASC,"
	orderings = orderings[:-1]
	print(f"""SELECT {', '.join(columns)}
			{joinings}
			{orderings};
			""")
	try:
		c.execute(f"""SELECT {', '.join(columns)} {joinings} {orderings};""")
		print("\n" + tab.tabulate(c.fetchall(), columns, tablefmt='simple'))
	except sqlite3.OperationalError:
		print("hey either too many relationships or theres no direct relationship")


def add():
	pass


main()
