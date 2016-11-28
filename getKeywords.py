import sqlite3



def getKeywords(uid):
    DATABASE = "myData.db"
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    cursor = conn.execute('SELECT * FROM tweets where id = ?', (uid,))

    c.execute('CREATE TABLE IF NOT EXISTS keywords (entry_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id, Sports_Athletics, Seminar_Lecture_Colloquium, Religious_National_Observances,Academic_Calendar, Institute_Holidays, Training_Workshop, Student_sponsored, Other_Miscellaneous, Conference_Symposium, Career_Professional_Development,Arts_Performance,Special);')
    c.execute("INSERT or replace INTO keywords (entry_id, user_id, Sports_Athletics, Seminar_Lecture_Colloquium, Religious_National_Observances,Academic_Calendar, Institute_Holidays, Training_Workshop, Student_sponsored, Other_Miscellaneous, Conference_Symposium, Career_Professional_Development,Arts_Performance,Special) VALUES((select entry_id from keywords where user_id = ?),?,'false','false','false','false','false','false','false','false','false','false','false','false')", (uid,uid,))

    kwords = {};
    for row in cursor:
        kwords = row["tweet"]
        if kwords.find("sport") != -1 or kwords.find("athletic") != -1:
            c.execute("UPDATE keywords SET Sports_Athletics=? WHERE user_id=?", ('true', uid))
        if kwords.find("art") != -1 or kwords.find("performance") != -1:
            c.execute("UPDATE keywords SET Arts_Performance=? WHERE user_id=?", ('true', uid))
        if kwords.find("career") != -1 or kwords.find("professional development") != -1:
            c.execute("UPDATE keywords SET Career_Professional_Development=? WHERE user_id=?", ('true', uid))
        if kwords.find("conference") != -1 or kwords.find("symposium") != -1:
            c.execute("UPDATE keywords SET Conference_Symposium=? WHERE user_id=?", ('true', uid))
        if kwords.find("miscellaneous") != -1:
            c.execute("UPDATE keywords SET Other_Miscellaneous=? WHERE user_id=?", ('true', uid))
        if kwords.find("student") != -1 and kwords.find("sponsor") != -1:
            c.execute("UPDATE keywords SET Student_sponsored=? WHERE user_id=?", ('true', uid))
        if kwords.find("training") != -1 or kwords.find("workshop") != -1:
            c.execute("UPDATE keywords SET Training_Workshop=? WHERE user_id=?", ('true', uid))
        if kwords.find("holiday") != -1:
            c.execute("UPDATE keywords SET Institute_Holidays=? WHERE user_id=?", ('true', uid))
        if kwords.find("academic") != -1 and kwords.find("calendar") != -1:
            c.execute("UPDATE keywords SET Academic_Calendar=? WHERE user_id=?", ('true', uid))
        if kwords.find("religious") != -1 or kwords.find("national observance") != -1:
            c.execute("UPDATE keywords SET Religious_National_Observances=? WHERE user_id=?", ('true', uid))
        if kwords.find("seminar") != -1 or kwords.find("lecture") != -1 or kwords.find("colloquium") != -1:
            c.execute("UPDATE keywords SET Seminar_Lecture_Colloquium=? WHERE user_id=?", ('true', uid))
        else:
            c.execute("UPDATE keywords SET Special=? WHERE user_id=?", ('true', uid))
        
        



    conn.commit()
    print ("Find keywords successfully");
    conn.close()
