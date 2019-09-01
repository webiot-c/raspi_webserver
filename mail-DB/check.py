import sqlite3

conn = sqlite3.connect('mail.db')
c = conn.cursor()

c.execute('SELECT * FROM data;')

print(c.fetchall())

#c.close()
conn.close()
