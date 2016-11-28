import sqlite3



def getKeywords():
    DATABASE = "myData.db"
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    cursor = conn.execute('SELECT * FROM tweets')


    kwords = {};
    for row in cursor:
        kwords = row["tweet"]
        if kwords.find("sport") != -1 or kwords.find("athletic") != -1:
            c.execute("UPDATE keywords SET bool = 'ture' where entry_id = 12")
        if kwords.find("art") != -1 or kwords.find("performance") != -1:
            c.execute("UPDATE keywords SET bool = 'ture' where entry_id = 2")
        if kwords.find("career") != -1 or kwords.find("professional development") != -1:
            c.execute("UPDATE keywords SET bool = 'ture' where entry_id = 3")
        if kwords.find("conference") != -1 or kwords.find("symposium") != -1:
            c.execute("UPDATE keywords SET bool = 'ture' where entry_id = 4")
        if kwords.find("miscellaneous") != -1:
            c.execute("UPDATE keywords SET bool = 'ture' where entry_id = 5")
        if kwords.find("student") != -1 and kwords.find("sponsor") != -1:
            c.execute("UPDATE keywords SET bool = 'ture' where entry_id = 6")
        if kwords.find("training") != -1 or kwords.find("workshop") != -1:
            c.execute("UPDATE keywords SET bool = 'ture' where entry_id = 7")
        if kwords.find("holiday") != -1:
            c.execute("UPDATE keywords SET bool = 'ture' where entry_id = 8")
        if kwords.find("academic") != -1 and kwords.find("calendar") != -1:
            c.execute("UPDATE keywords SET bool = 'ture' where entry_id = 9")
        if kwords.find("religious") != -1 or kwords.find("national observance") != -1:
            c.execute("UPDATE keywords SET bool = 'ture' where entry_id = 10")
        if kwords.find("seminar") != -1 or kwords.find("lecture") != -1 or kwords.find("colloquium") != -1:
            c.execute("UPDATE keywords SET bool = 'ture' where entry_id = 11")
        else:
            c.execute("UPDATE keywords SET bool = 'ture' where entry_id = 1")
        
        



    conn.commit()
    print ("Find keywords successfully");
    conn.close()
