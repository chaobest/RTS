import feedparser     # available at http://feedparser.org
import sqlite3


def getEventInfo():
    DATABASE = "myData.db"
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    #nsert initial values into feed database
    c.execute('DROP TABLE IF EXISTS RSSEntries;')
    #c.execute('CREATE TABLE IF NOT EXISTS RSSFeeds (id INTEGER PRIMARY KEY AUTOINCREMENT, url VARCHAR(1000));')
    c.execute('CREATE TABLE IF NOT EXISTS RSSEntries (entry_id INTEGER PRIMARY KEY AUTOINCREMENT, url, title, category);')

    titleContent = []
    linkContent = []
    categoryContent = []

    d = feedparser.parse('http://www.calendar.gatech.edu/feeds/events.xml')
    for item in d.entries:
        #print (item['title'])
        #print (item['link'])
        # inside your loop to add items:
        if (item['title']) not in titleContent:
            titleContent.append(item['title'])
            linkContent.append(item['link'])
            print (item['category'])
        #    categoryContent.append(item['category'])
    print ("--------")

    array_length = len(titleContent);

    for i in range(array_length):
        c.execute('INSERT INTO RSSEntries (url, title, category) VALUES (?,?,?)', (linkContent[i], titleContent[i],categoryContent[i]))

    conn.commit()
    print ("Records created successfully");
    conn.close()