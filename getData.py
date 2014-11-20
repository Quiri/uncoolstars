import os
from facepy import GraphAPI
import sqlite3
import time


token = os.environ["uncoolstars"]
graph = GraphAPI(token)

conn = sqlite3.connect('uncoolstars.db')

def getFromFB(star):
    try:
        data = graph.get(star + "?fields=name,likes,talking_about_count,is_verified,username,id,category")
   # except OAuthError as oauth:
    #    return star * "not a public profile"
    except:
        return "Could not get account " + star
    
    if(not data["is_verified"]):
        return "Not verified"
    else:
        return data

def addEntry(star):
    data = getFromFB(star)
    if (type(data) is str):
        return False
    else:
        insert = [data["likes"],data["name"],data["talking_about_count"],data["username"], time.strftime("%Y-%m-%d"), time.strftime("%c")]
        c = conn.cursor()
        c.execute("insert into likes values(?,?,?,?,?,?)", insert)
        c.close()
        conn.commit()
        return True

def getAllStars():
    c = conn.cursor()
    c.execute("SELECT distinct username FROM stars")
    return c.fetchone()

def isStarinDB(star):
    c = conn.cursor()
    star = (star,)
    c.execute("Select count(*) FROM stars Where username = ?", star)
    result = c.fetchone()
    return result[0] == 1 

def addStar(star):
    if isStarinDB(star):
        print star + " is already in DB"
        return  False

    data = getFromFB(star)

    if (type(data) is str):
        return False
    
    insert = [data["id"], data["category"], data["username"], time.strftime("%c")]
    c = conn.cursor()
    c.execute("INSERT into stars values(?,?,?,?)", insert)
    c.close()
        
    addEntry(star)

    return True

def addNewStar(star):
    addEntry(star)
    
