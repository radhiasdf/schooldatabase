from constants import *
import search


def printEnterBackKey():
	print(f"-Enter '{backkey}' to go back-")


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
		ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		StudentID INTEGER NOT NULL,
		ClassID INTEGER NOT NULL,
		FOREIGN KEY (StudentID) REFERENCES Students(ID),
		FOREIGN KEY (ClassID) REFERENCES Classes(ID)
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
				c.execute(f"""INSERT INTO {tablename} ({columnNames}) 
							VALUES ({('?,' * len(row))[:-1]});""", tuple(row))


def printTable(table):
	c.execute(f"SELECT * FROM {table};")
	display = c.fetchall()
	c.execute(f"PRAGMA table_info({table});")
	headers = [column[1] for column in c.fetchall()]
	print("\n" + tab.tabulate(display, headers, tablefmt='simple'))

def modify():
	for i, table in enumerate(tables):
		print(f"{i+1}. {table}")
	while True:
		try:
			inp = input("ok which table do you want to modify (enter number): ")
			if inp == backkey:
				return backkey
			table = tables[int(inp) - 1]
			c.execute(f"SELECT * FROM {table};") # to catch errors
			break
		except ValueError:
			pass
		except IndexError:
			pass
	printTable(table)

	while True:
		action = input("ok now do u want to edit (1), add (2), or remove (3): ")
		if action == backkey:
			break
		while True:
			if action == '1':
				if edit(table) == backkey:
					break
			elif action == '2':
				if add(table) == backkey:
					break
			elif action == '3':
				if remove(table) == backkey:
					break
			else:
				break

def edit(table):
	row = input("enter which row to edit: ")
	if row == backkey:
		return backkey
	try:
		c.execute(f"PRAGMA table_info({table});")
		columnsInfo = c.fetchall()
		# it doesn't ask the user to put data for primary autoincrementing fields
		headersNoID = [header[1] for i, header in enumerate(columnsInfo) if columnsInfo[i][5] != 1]

		c.execute(f"SELECT * FROM {table} WHERE ID = {row};")
		print(', '.join(str(cell) for i, cell in enumerate(c.fetchall()[0]) if columnsInfo[i][5] != 1))
		newData = input(f"Enter new data in the format {', '.join(headersNoID)}:\n").split(',')
		columnToValue = ''.join([f"{header} = '{newData[i]}', " for i, header in enumerate(headersNoID)])[:-2]

		query = f"UPDATE {table} SET {columnToValue} WHERE ID = {row};"
		c.execute(query)
		printTable(table)
	except IndexError:
		print("row doesnt exist")

def add(table):
	c.execute(f"PRAGMA table_info({table});")
	columnsInfo = c.fetchall()
	headers = [column[1] for column in columnsInfo]
	# it doesn't ask the user to put data for primary autoincrementing fields
	headersNoID = [data for i, data in enumerate(headers) if columnsInfo[i][5] != 1]

	while True:
		inp = input(f"hey now enter the things exactly like {','.join(headersNoID)}: ")
		if inp == backkey:
			return backkey
		data = inp.split(',')
		if len(data) == len(headersNoID):
			break
		else:
			print("hey number of columns doesnt match")

	query = f"""INSERT INTO {table} ({','.join(headersNoID)}) 
							VALUES ({('?,' * len(headersNoID))[:-1]});"""
	c.execute(query, tuple(data))
	connect.commit()
	printTable(table)


def remove(table):
	row = input("enter the row number u want to remove: ")
	if row == backkey:
		return backkey
	try:
		c.execute(f"SELECT * FROM {table} WHERE ID = {row};")
		removedRow = ', '.join(str(cell) for cell in c.fetchall()[0])
		c.execute(f"DELETE FROM {table} WHERE ID = {row};")
		printTable(table)
		print(f"{removedRow} has been removed")
	except sqlite3.OperationalError:
		print("dude numbers")
	except IndexError:
		print("row doesnt exist")


if reset:
	resetTables()
	CSVtoDatabase("13 Databases data (1) - Classes.csv", "Classes")
	CSVtoDatabase("13 Databases data (1) - Students.csv", "Students")
	CSVtoDatabase("13 Databases data (1) - Students and Classes.csv", "StudentsAndClasses")
	CSVtoDatabase("13 Databases data (1) - Teachers.csv", "Teachers")

c.execute("""SELECT name FROM sqlite_schema WHERE type ='table' 
AND name NOT LIKE 'sqlite_%';""")
tables = [table[0] for table in c.fetchall()]

while True:
	printEnterBackKey()
	action = input("hey do u want to search (1) or modify (2): ")
	if action == backkey:
		break
	while True:
		if action == '1':
			if search.askFields(tables) == backkey:
				break
		elif action == '2':
			if modify() == backkey:
				break
		else:
			break
