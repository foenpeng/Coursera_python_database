# This program extract information from a json file and construct a many to many relational sqlite database

import json
import sqlite3

conn = sqlite3.connect('roster.sqlite')
cur = conn.cursor()

fname = raw_input("which roster? ")
if len(fname) <1 : fname = 'roster_data.json'
str_name = open(fname).read()
json_data = json.loads(str_name)

cur.executescript('''
  CREATE TABLE IF NOT EXISTS User(
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  name TEXT UNIQUE);
  
  CREATE TABLE IF NOT EXISTS Course(
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  title TEXT UNIQUE);  
  
  CREATE TABLE IF NOT EXISTS Member(
  user_id INTEGER,
  course_id INTEGER,
  role INTEGER,
  PRIMARY KEY (user_id, course_id))
''')

for entry in json_data:
  user = str(entry[0])
  title = str(entry[1])
  role = int(entry[2])
  print(user, title, role)
  
  cur.execute('''INSERT OR IGNORE INTO User(name) VALUES(?)''',(user,))
  cur.execute('''SELECT id FROM User WHERE name = ?''',(user,))
  user_id = cur.fetchone()[0]

  
  cur.execute('''INSERT OR IGNORE INTO Course (title) VALUES (?)''',(title,))
  cur.execute('''SELECT id FROM Course WHERE title = ?''',(title,))
  course_id = cur.fetchone()[0]
  
  cur.execute('''INSERT OR REPLACE INTO Member(user_id, course_id, role) VALUES(?,?,?)''',(user_id, course_id, role))
     
  conn.commit()
  
  