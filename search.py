from constants import *


def askFields(tables):
	# printing out available columns across all tables, with numbers assigned for each column
	tables = [table for table in tables if table != 'StudentsAndClasses']
	for i, table in enumerate(tables):
		print(f"{i + 1}: {table}")

	# ask for which fields to display, and parse input. try check for valid column numbers
	while True:
		try:
			inp = input("Enter table(s), eg. 2,1 for every student's classes:")
			if inp == backkey:
				return backkey
			selectedTables = [tables[int(i) - 1] for i in inp.split(',')]
			break
		except ValueError:
			pass
		except KeyError:
			pass

	printAndFilter(selectedTables)


def printAndFilter(selectedTables):
	# translating into sql and printing it out
	headers = []
	selectedColumns = []
	for table in selectedTables:
		c.execute(f"PRAGMA table_info({table});")
		for column in c.fetchall():
			headers.append(column[1])
			selectedColumns.append(f"{table}.{column[1]}")

	joinings = ""
	for i in range(len(selectedTables)):
		if i + 1 >= len(selectedTables):
			break
		link = (selectedTables[i], selectedTables[i + 1])
		if link == ('Teachers', 'Classes'):
			joinings += " JOIN Classes ON Teachers.ID = Classes.TeacherID"
		elif link == ('Classes', 'Teachers'):
			joinings += " JOIN Teachers ON Teachers.ID = Classes.TeacherID"
		elif link == ('Classes', 'Students'):
			joinings += """ JOIN StudentsAndClasses ON Classes.ID = StudentsAndClasses.ClassID
			JOIN Students ON StudentsAndClasses.StudentID = Students.ID """
		elif link == ('Students', 'Classes'):
			joinings += """ JOIN StudentsAndClasses ON Students.ID = StudentsAndClasses.StudentID
			JOIN Classes ON StudentsAndClasses.ClassID = Classes.ID """

	orderBy = "ORDER BY"
	for column in selectedColumns:
		orderBy += f" {column} ASC,"
	orderBy = orderBy[:-1]

	filters = ""
	while True:
		query = f"""SELECT {','.join(selectedColumns)} FROM {selectedTables[0]} {joinings} {filters} {orderBy};"""
		try:
			c.execute(query)
			display = c.fetchall()
			print("\n" + tab.tabulate(display, selectedColumns, tablefmt='simple'))
			if len(selectedTables) > 1:
				print("Ok so this is joined up RELATIONSHIP display")

			filters = inp = input(f"Search for something if you want: ")
			if inp == backkey:
				break
			filters = "WHERE " + ' '.join([f"{column} LIKE '%{filters}%' OR" for column in selectedColumns])[:-3]

		except sqlite3.OperationalError as e:
			print(f"Hey error of {e}")
			if 'no such column' in str(e):
				print("There isn't a direct relationship between teacher and student")
			break
