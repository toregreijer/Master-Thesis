__author__ = 'joakim'
import sqlite3

sqlite_file = 'the_great_db.sqlite'
table1 = 'house001'
field1 = 'unit_name'
field2 = 'datetime'
field3 = 'value'

# FIND AND OPEN THE DATABASE,
# IF NONE EXISTS, CREATE A NEW ONE.
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

# Creating a new SQLite table with 3 columns
# c.execute('CREATE TABLE {tn} ({fn1} {ft1} PRIMARY KEY, {fn2} {ft2}, {fn3} {ft3})'
#         .format(tn=table1, fn1=field1, ft1='TEXT', fn2=field2, ft2='TEXT', fn3=field3, ft3='INTEGER'))

# Committing changes and closing the connection to the database file
# conn.commit()
conn.close()
