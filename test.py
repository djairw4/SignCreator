import sqlite3

db = sqlite3.connect(r'C:\IPG\carmaker\win64-10.1\TrafficSigns\DEU\Images.db')
# creating cursor
cur = db.cursor()
cur.execute("SELECT name FROM sqlite_master")
# reading all table names
table_list = [a for a in cur.execute("SELECT * FROM sqlite_master")]
# here is you table list
print(table_list)

# Be sure to close the connection
db.close()
NoOvertaking.png