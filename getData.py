import os
from facepy import GraphAPI
import sqlite3
import time
import re

home = os.environ["HOME"]
os.chdir(home + "/uncoolstars")

token = os.environ["uncoolstars"]
graph = GraphAPI(token)

conn = sqlite3.connect('uncoolstars.db')

def getFromFB(star):
    try:
        data = graph.get(star + "?fields=name,likes,talking_about_count,is_verified,username,id,category")
   # except OAuthError as oauth:
    #    return star * "not a public profile"
    except:
        return "Could not get account " + star + "."
    
    if(not data["is_verified"]):
        return "Account " + star + "is not verified."
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
    c.close()
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


def oldpost(id):
    c = conn.cursor()
    id = (id,)
    c.execute("Select count(*) FROM requests WHERE id = ?", id)
    result = c.fetchone()
    c.close()
    return result[0] == 1



def addFromFeed():
    feed = graph.get("me/feed?limit=100")
    for post in feed["data"]:
        if ("message" in post.keys()):
            if len(re.findall("^add ", post["message"])) == 1:
                if (not oldpost(post["id"])):
                    star = re.split(" ", post["message"])[1]
                    fromfb = getFromFB(star)
                    if(type(fromfb) is str) :
                        graph.post(path=post["id"]+"/comments", message=fromfb)
                        print "Request not valid " + post["message"]
                    else:
                        newstar = not isStarinDB(star)
                        ins = [post["id"], post["message"], post["from"]["id"], post["from"]["name"], post["created_time"], time.strftime("%c"), newstar]

                        c = conn.cursor()
                        c.execute("INSERT into requests values(?,?,?,?,?,?,?)",ins)
                        c.close()
                    
                        if (newstar):
                            addStar(star)
                            mess = star + " added to DB and started watching"
                            graph.post(path=post["id"]+"/comments",message= mess)
                            print mess
                        else:
                            conn.commit()
                            c = conn.cursor()
                            c.execute("Select inserted from stars where username = ?", (star,))
                            inDBsince = c.fetchone()[0]
                            c.close()
                            mess = star + " is already in db since " + inDBsince
                            print mess
                            graph.post(path=post["id"]+"/comments",message = mess)
    return True


