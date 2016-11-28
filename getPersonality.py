from os.path import join, dirname
from watson_developer_cloud import PersonalityInsightsV3
import json
import sqlite3

def getPersonality(name):
    personality_insights = PersonalityInsightsV3(
      version='2016-10-20',
      username='55517bfe-4325-4b1d-9594-13e509be7e27',
      password='bigX423dj5B8')

    with open(join(dirname(__file__), './tweets_%s.txt' % name)) as profile_txt:
      profile = personality_insights.profile(
        profile_txt.read(), content_type='text/plain',
        raw_scores=True, consumption_preferences=True)

    print(json.dumps(profile, indent=2))
    with open('personality_%s.json' % name, 'w') as fp:
        json.dump(profile, fp)
    #print(profile['values'][0]['percentile'])

    #----------write to database--------------
    DATABASE = "myData.db"
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute('CREATE TABLE IF NOT EXISTS personality (entry_id INTEGER PRIMARY KEY AUTOINCREMENT, id, openness, conscientiousness, extraversion, agreeableness, neuroticism, conservation, openness_to_change, hedonism, self_enhancement, self_transcendence);')
    cursor = conn.execute('SELECT entry_id FROM users where username = (?)', (name,))    
    for row in cursor:
        user_id = row[0]
    #print(user_id)
    c.execute('insert or replace INTO personality (entry_id, id, openness, conscientiousness, extraversion, agreeableness, neuroticism, conservation, openness_to_change, hedonism, self_enhancement, self_transcendence) VALUES ((select entry_id from personality where id = ?), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);', (user_id, user_id, profile['personality'][0]['percentile'], profile['personality'][1]['percentile'], profile['personality'][2]['percentile'], profile['personality'][3]['percentile'], profile['personality'][4]['percentile'], profile['values'][0]['percentile'], profile['values'][1]['percentile'], profile['values'][2]['percentile'], profile['values'][3]['percentile'], profile['values'][4]['percentile']))
    conn.commit()
    print ("Personality Records created successfully");
    conn.close()
