from getData import *

c = conn.cursor()
c.execute("Select username FROM stars")
stars = c.fetchall()

for star in stars:
    addEntry(star[0])
