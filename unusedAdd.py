def tediousUnusedAdd(fields):
	print(fields)
	while True:
		# it doesn't ask the user to put data for primary autoincrementing fields
		inp = input(f"hey now enter the things exactly like {','.join(fields)}: ")
		if inp == backkey:
			return backkey
		data = inp.split(',')
		if len(data) == len(fields):
			break
		else:
			print("hey number of columns doesnt match")

	selectedtables = getSelectedTables(fields)
	if 'Students' in selectedtables and 'Classes' in selectedtables:

		query = f"""SELECT Students.ID FROM Students WHERE"""
		for i in range(len(fields)):
			if "Students" in fields[i]:
				query += f" {fields[i]} LIKE '%{data[i]}%' AND"
		query = query.strip(" AND")
		query += ","
		query += f"""SELECT Classes.ID FROM Classes WHERE"""
		for i in range(len(fields)):
			if "Classes" in fields[i]:
				query += f" {fields[i]} LIKE '%{data[i]}%' AND"
		query = query.strip(" AND")
		query += ";"

		print(query)
		c.execute(query, tuple(data))
		print("\n" + tab.tabulate(c.fetchall(), fields, tablefmt='simple'))
	connect.commit()
