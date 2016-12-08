import sqlite3
import xml.etree.ElementTree as ET

conn = sqlite3.connect('track.sqlite')
cur = conn.cursor()

cur.executescript('''
  DROP TABLE IF EXISTS Artist;
  DROP TABLE IF EXISTS Album;
  DROP TABLE IF EXISTS Track;
  DROP TABLE IF EXISTS Genre;
  
  CREATE TABLE Artist (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  name TEXT UNIQUE);
  
  
  CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE);
  
  CREATE TABLE Album (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  artist_id INTEGER,
  title TEXT UNIQUE);
  
  CREATE TABLE Track (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
  title TEXT UNIQUE,
  album_id INTEGER,
  genre_id INTEGER,
  len INTEGER,
  count INTEGER,
  rating INTEGER);
    ''')

def lookup(t,key):
 found = None;
 for child in t:
   if found == True: return child.text
   if child.tag == 'key' and child.text == key :
     found = True
 return None
   
   
fname = raw_input("File to execute? ")
if len(fname) < 1: fname = "Library.xml"

content = ET.parse(fname)
all = content.findall("dict/dict/dict")
for entry in all:
    if lookup(entry, 'Track ID') is None: continue
  
    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')
    genre = lookup(entry,'Genre')
    
    if name is None or artist is None or album is None or genre is None: continue
    
    cur.execute('''INSERT OR IGNORE INTO Artist (
    name) VALUES (?)''',(artist,))
    cur.execute('''SELECT id FROM Artist WHERE name = ?''',(artist,))
    artist_id = cur.fetchone()[0]
    
    cur.execute('''INSERT OR IGNORE INTO Album (
    artist_id, title) VALUES (?,?)''',(artist_id,album))
    cur.execute('''SELECT id FROM Album WHERE title = ?''',(album,))
    album_id = cur.fetchone()[0]
    
    cur.execute('''INSERT OR IGNORE INTO Genre (
    name) VALUES (?)''',(genre,))
    cur.execute('''SELECT id FROM Genre WHERE name = ?''',(genre,))
    genre_id = cur.fetchone()[0]
    
    cur.execute('''INSERT OR REPLACE INTO Track (
    title,album_id,genre_id,len, count,rating)
     VALUES (?,?,?,?,?,?)''',(name, album_id, genre_id, length, count, rating))
     
    conn.commit()
     
cur.close()
    
