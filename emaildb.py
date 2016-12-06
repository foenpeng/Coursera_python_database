import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS Counts ''')
cur.execute('''CREATE TABLE Counts (org TEXT, count INTEGER)''')

filename = raw_input("which file to execute? ")
file = open(filename)

for line in file:
  if not line.startswith('From: '): continue
  pieces = line.split()
  piece = pieces[1]
  domain = piece[piece.find("@") + 1:]
  print domain
  cur.execute('''SELECT count FROM Counts WHERE org = ?''',(domain,))
  org = cur.fetchone()
  if org is None:
    cur.execute('''INSERT INTO Counts (org, count) VALUES(?, 1)''',(domain,))
  else:
    cur.execute('''UPDATE Counts SET count = count +1 WHERE org = ?''',(domain,))
  conn.commit()
  
sqlitestr = '''SELECT org, count FROM COUNTS ORDER BY count DESC limit 10'''

for row in cur.execute(sqlitestr):
  print(row)
  
cur.close()