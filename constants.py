import sqlite3
import csv
import tabulate as tab

reset = True

backkey = "<"
connect = sqlite3.connect('Database.db')
c = connect.cursor()