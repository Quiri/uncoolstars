from getData import *

c = conn.cursor()
c.execute("Select username FROM stars")
stars = c.fetchall()

allstars = 0
updatedstars = 0

for star in stars:
    allstars = allstars + 1
    try:
	addEntry(star[0])
	updatedstars = updatedstars + 1
    except:
	print star[0] + " could not be updated"

print "Updated" ,  updatedstars , "out of" ,  allstars , "stars."

