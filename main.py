import sqlite3
import csv
import tabulate as tab
import itertools

# import replit

backkey = "<"


def update():
    # replit.clear()
    print("-Enter '" + backkey + "' to go back-")


# Inserting data from the csvs to the databases
def InsertCSVs():
    with open("maori trees - Sheet1.csv", "r") as file:
        for row in csv.reader(file):
            c.execute("""INSERT INTO Trees (ID, MaoriName, Reference, ScientificName) 
						VALUES (?, ?, ?, ?);""", (row[0], row[1], row[2], row[3]))

    with open("people.csv", "r") as file:
        for row in csv.reader(file):
            c.execute("""INSERT INTO People (ID, FirstName, LastName, Email) 
						VALUES (?, ?, ?, ?);""", (row[0], row[1], row[2], row[3]))
    with open("persontotree.csv", "r") as file:
        for row in csv.reader(file):
            c.execute("""INSERT INTO Relations (PersonID, TreeID) 
						VALUES (?, ?);""", (row[1], row[2]))  # needs to be second and third row


def check_input(text, type, rangeend):
    inp = input(text).strip()
    if inp == backkey:
        return backkey
    if type == "int":
        try:
            inp = int(inp)
            if inp in range(1, rangeend):
                return inp
            else:
                return False
        except:
            return False


connect = sqlite3.connect('Database.db')
c = connect.cursor()

tree_fields = ["ID", "MaoriName", "Reference", "ScientificName"]
people_fields = ["ID", "FirstName", "LastName", "Email"]
relations_fields = ["ID", "PersonID", "TreeID"]

# This sets the thing
try:
    c.execute("SELECT * FROM Trees;")
    print('already there')
except sqlite3.OperationalError:
    print('nope')
    # Resetting tables bc duplication error
    c.execute("DROP TABLE IF EXISTS 'Trees';")
    c.execute("DROP TABLE IF EXISTS 'People';")
    c.execute("DROP TABLE IF EXISTS 'Relations';")
    # Creating tables
    c.execute("""
	CREATE TABLE Trees (
		ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		MaoriName TEXT NOT NULL,
		Reference TEXT NOT NULL,
		ScientificName TEXT NOT NULL
	);
	""")
    c.execute("""
	CREATE TABLE People (
		ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		FirstName TEXT NOT NULL,
		LastName TEXT NOT NULL,
		Email TEXT NOT NULL
	);
	""")
    c.execute("""
	CREATE TABLE Relations (
		ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
		PersonID INTEGER NOT NULL,
		TreeID INTEGER NOT NULL,
		FOREIGN KEY (PersonID) REFERENCES People(ID),
		FOREIGN KEY (TreeID) REFERENCES Tree(ID)
	);
	""")
    InsertCSVs()
    connect.commit()

tables = ["Trees", "People"]
fields = ["Trees.ID", "Trees.MaoriName", "Trees.Reference", "Trees.ScientificName",
          "People.ID", "People.FirstName", "People.LastName", "People.Email",
          "Relations.ID", "Relations.PersonID", "Relations.TreeID"]


def main():
    while True:
        for i, field in enumerate(fields):
            print(f"{i + 1}. {field}")
        while True:
            action = "hey do you want to search something (1) or add something (2): "
            try:
                if int(action) == 1:
                    search()
                elif int(action) == 2:
                    add()
            except ValueError:
                pass


def search():
    selected = input("hey lets enter some specific columns you want to search stuff in, eg. 1,2,3: ")
    c.execute(f"""SELECT {', '.join(selected)}
			FROM Relations
			INNER JOIN People ON People.ID = Relations.PersonID
			INNER JOIN Trees ON Trees.ID = Relations.TreeID;
			""")
    print("\n" + tab.tabulate(c.fetchall(), selected, tablefmt='simple'))


def add():
    pass


main()
