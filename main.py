import sqlite3
import csv
import tabulate as tab

reset = True

backkey = "<"

connect = sqlite3.connect('Database.db')
c = connect.cursor()


def update():
	print("-Enter '" + backkey + "' to go back-")


# This sets the thing
def resetTables():
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
	connect.commit()


def CSVtoDatabase(filename, tablename):
	with open(filename, "r") as file:
		columnNames = ','.join(next(csv.reader(file)))
		for i, row in enumerate(csv.reader(file)):
			if i > 0:
				c.execute(f"""INSERT INTO {tablename} ({columnNames}) 
							VALUES ({('?,' * len(row))[:-1]});""", tuple(row))


def main():
	while True:
		action = input("(Enter '<' to go back)\nhey do you want to search something (1) or add something (2): ")
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
			selected = inp = input("hey lets enter some specific columns you want to search stuff in, eg. 1,2,3: ")
			if inp == backkey:
				return
			columns = [columnDict[int(i)] for i in selected.split(",")]
			print(', '.join(columns))
			selectedtables = [column.split('.', 1)[0] for column in columns]
			break
		except ValueError:
			pass
		except KeyError:
			pass

	joinings = ""
	fromm = ""
	if 'Students' in selectedtables and 'Classes' in selectedtables:
		fromm = "FROM StudentsAndClasses"
		joinings += """
		INNER JOIN Students ON Students.ID = StudentsAndClasses.StudentID
		INNER JOIN Classes ON Classes.ID = StudentsAndClasses.ClassID"""
	if 'Teachers' in selectedtables and 'Classes' in selectedtables:
		fromm = "FROM Classes"
		joinings += """
		INNER JOIN Teachers ON Teachers.ID = Classes.TeacherID"""
	if fromm == "":
		fromm = f"FROM {selectedtables[0]}"

	orderings = "ORDER BY"
	for column in columns:
		orderings += f" {column} ASC,"
	orderings = orderings[:-1]
	query = f"""SELECT {', '.join(columns)} {fromm} {joinings} {orderings};"""
	print(query)
	c.execute(query)
	print("\n" + tab.tabulate(c.fetchall(), columns, tablefmt='simple'))


def add():
	for i, table in enumerate(tables):
		print(f"{i + 1}. {table[0]}")
	while True:
		try:
			inp = input("hey which table do you want to add in: ")
			if inp == backkey:
				return
			num = int(inp) - 1
			break
		except ValueError:
			pass
		except IndexError:
			pass
	while True:
		c.execute(f"SELECT * FROM {tables[num][0]};")
		display = c.fetchall()
		c.execute(f"PRAGMA table_info({tables[num][0]});")
		headers = [column[1] for column in c.fetchall()]
		print("\n" + tab.tabulate(display, headers, tablefmt='simple'))

		headersNoID = [data for data in headers if data != 'ID']
		inp = input(f"hey now enter the things in the format {','.join(headersNoID)}: ")
		if inp == backkey:
			return
		data = inp.split(',')
		if len(data) != len(headersNoID):
			print("hey number of columns doesnt match")
			continue
		query = f"""INSERT INTO {tables[num][0]} ({','.join(headersNoID)}) 
								VALUES ({('?,' * len(headersNoID))[:-1]});"""
		c.execute(query, tuple(data))
		connect.commit()


if reset:
	resetTables()
	CSVtoDatabase("13 Databases data (1) - Classes.csv", "Classes")
	CSVtoDatabase("13 Databases data (1) - Students.csv", "Students")
	CSVtoDatabase("13 Databases data (1) - Students and Classes.csv", "StudentsAndClasses")
	CSVtoDatabase("13 Databases data (1) - Students with timetables.csv", "StudentsWithTimetables")
	CSVtoDatabase("13 Databases data (1) - Teachers.csv", "Teachers")

c.execute("""SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';""")
tables = c.fetchall()

main()
