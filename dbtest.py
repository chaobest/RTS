import sqlite3

if __name__ == '__main__':
    DATABASE = "myData.db"
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
	
    ROOT_USER = "PoloChau"

    #c.execute('DROP TABLE IF EXISTS personality;')
    c.execute('CREATE TABLE IF NOT EXISTS personality (entry_id INTEGER PRIMARY KEY AUTOINCREMENT, id, openness, conscientiousness, extraversion);')
    cursor = conn.execute('SELECT entry_id FROM users where username = (?)', (ROOT_USER,))    
    for row in cursor:
        user_id = row[0]
    print(user_id)
    c.execute('insert or replace INTO personality (entry_id, id, openness, conscientiousness, extraversion) VALUES ((select entry_id from personality where id = ?), ?, ?, ?, ?);', (user_id, user_id, 1,2,2))
    #c.execute('insert or replace INTO personality (id, openness, conscientiousness, extraversion) VALUES (?, ?,?,?);', (user_id,1,2,3))

    conn.commit()
    print ("Records created successfully");
    conn.close()