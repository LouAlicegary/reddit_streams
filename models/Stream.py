import time

from utils import Logger



"""
Inserts a stream into the streams table
"""
def create(stream, db) :

    connection = db['connection']
    cursor = db['cursor']

    format_str = """ SELECT * FROM streams WHERE url LIKE "{url}" AND source_id LIKE "{source_id}"; """
    sql_command = format_str.format(url = stream["url"], source_id = stream['source_id'])
    cursor.execute(sql_command)

    results = cursor.fetchall()
    result_count = len(results) if (results is not None) else 0 

    if result_count == 0:
        
        Logger.log_level("Creating stream.", 1)
        Logger.log_level("Rating: " + str(stream['rating']) + " Provider: " + stream['provider'] + " URL: " + stream['url'], 2)

        format_str = """ INSERT OR REPLACE INTO streams (url, source_type, source_id, provider, created_at, quality, language, rating) VALUES ("{url}", "{source_type}", "{source_id}", "{provider}", datetime("{created_at}"), "{quality}", "{language}", "{rating}"); """
        sql_command = format_str.format(url = stream['url'], source_type = stream['source_type'], source_id = stream['source_id'], provider = stream['provider'], created_at = stream['created_at'], quality = stream['quality'], language = stream['language'], rating = stream['rating'])
        cursor.execute(sql_command)
        connection.commit()
    
    else: 
        
        Logger.log_level("Stream already exists.", 1)
        Logger.log_level("Rating: " + str(stream['rating']) + " Provider: " + stream['provider'] + " URL: " + stream['url'], 2)






"""
Drop and create the comments table (for first-level comments to a Reddit post)
"""
def create_table(db) :

    connection = db['connection']
    cursor = db['cursor']
    
    # Create streams table
    cursor.execute('''DROP TABLE IF EXISTS streams''')
    
    cursor.execute('''CREATE TABLE streams (
        url text, 
        source_type text,
        source_id text,
        provider text, 
        created_at datetime, 
        quality text,      
        language text,
        rating real
    )''')

    # Commit all the DB operations
    connection.commit()
