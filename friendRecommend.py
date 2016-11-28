import sqlite3
from collections import OrderedDict


#root_user = 'PoloChau'
def friendRecommend(root_user):
    DATABASE = "myData.db"
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    cursor = conn.execute('SELECT entry_id FROM users where username = (?)', (root_user,))    
    for row in cursor:
        my_id = row[0]


    myPersonality = {}
    c.execute('SELECT * from personality WHERE id = (?)', (my_id,))
    for row in c:
        myPersonality["openness"] = row["openness"]
        myPersonality["conscientiousness"] = row["conscientiousness"]
        myPersonality["extraversion"] = row["extraversion"]
        myPersonality["agreeableness"] = row["agreeableness"]
        myPersonality["neuroticism"] = row["neuroticism"]
        myPersonality["conservation"] = row["conservation"]
        myPersonality["openness_to_change"] = row["openness_to_change"]
        myPersonality["hedonism"] = row["hedonism"]
        myPersonality["self_enhancement"] = row["self_enhancement"]
        myPersonality["self_transcendence"] = row["self_transcendence"] 
    print(myPersonality)


    PersonalityDiff = {}
    PersonalityRankedDiff = {}

    c.execute('CREATE TABLE IF NOT EXISTS recommended_friend (entry_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id, Fridnd_No, friend_name)')
    cursor = conn.execute('SELECT * from personality')
    for row in cursor:
        user_id = row["id"]

        #continue
        if user_id != my_id:
            c.execute('SELECT * from personality WHERE id = (?)', (user_id,))
            for row in c:
                PersonalityDiff["openness"] = myPersonality["openness"] - row["openness"]
                PersonalityDiff["conscientiousness"] = myPersonality["conscientiousness"] - row["conscientiousness"]
                PersonalityDiff["extraversion"] = myPersonality["extraversion"] - row["extraversion"]
                PersonalityDiff["agreeableness"] = myPersonality["agreeableness"] - row["agreeableness"]
                PersonalityDiff["neuroticism"] = myPersonality["neuroticism"] - row["neuroticism"]
                PersonalityDiff["conservation"] = myPersonality["conservation"] - row["conservation"]
                PersonalityDiff["openness_to_change"] = myPersonality["openness_to_change"] - row["openness_to_change"]
                PersonalityDiff["hedonism"] = myPersonality["hedonism"] - row["hedonism"]
                PersonalityDiff["self_enhancement"] = myPersonality["self_enhancement"] - row["self_enhancement"]
                PersonalityDiff["self_transcendence"] = myPersonality["self_transcendence"] - row["self_transcendence"]
            diff = sum(PersonalityDiff.values())
            PersonalityRankedDiff[user_id] = diff

    sortedList = []
    print(PersonalityRankedDiff)

    sortedL = [(k, PersonalityRankedDiff[k]) for k in sorted(PersonalityRankedDiff, key=PersonalityRankedDiff.get, reverse=True)]
    counter = 0;
    for k, v in sortedL:
        counter = counter + 1
        if counter <= 5 and v >= -2.5:
            cursor = conn.execute('SELECT username FROM users where entry_id = (?,?)', (k,))    
            for row in cursor:
                friend_name = row[0]
                sortedList.append(friend_name)
                c.execute('insert or replace INTO recommended_friend (entry_id, user_id, Fridnd_No, friend_name) VALUES ((select entry_id from recommended_friend where user_id = ? AND Fridnd_No = ?), ?, ?, ?);', (my_id, counter, my_id, counter, friend_name))

    print(sortedList)



    conn.commit()
    print ("Personality recommended successfully");
    conn.close()
