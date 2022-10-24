import sqlite3

connection = sqlite3.connect('database.db')

#use schema with payer(string), points (integer), timestamp (string)
#sqlite3 does not have date datatype so text will be used instead
with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

#add some sample data
cur.execute("INSERT INTO posts (payer, points, time) VALUES (?, ?, ?)",
            ('DANNON', 1000, '2020-11-02T14:00:00Z')
            )

cur.execute("INSERT INTO posts (payer, points, time) VALUES (?, ?, ?)",
            ('UNILEVER', 200, '2020-10-31T11:00:00Z')
             )

cur.execute("INSERT INTO posts (payer, points, time) VALUES (?, ?, ?)",
            ('DANNON', -200, '2020-10-31T15:00:00Z')
             )

cur.execute("INSERT INTO posts (payer, points, time) VALUES (?, ?, ?)",
            ('MILLER COORS', 10000, '2020-11-01T14:00:00Z')
             )

cur.execute("INSERT INTO posts (payer, points, time) VALUES (?, ?, ?)",
            ('DANNON', 300, '2020-10-31T10:00:00Z')
             )

#commit changes and close connection to the database
connection.commit()
connection.close()

