import html

from utils import Logger



"""
Insert record into streams table
"""
def create(x, db) :

    connection = db['connection']
    cursor = db['cursor']

    if x['user'] is not None:
        
        Logger.log_level("Comment created: From user " + x['user'], 3)

        # Build and execute SQL Insert query (uses new string interpolation method format() instead of % syntax)
        format_str = """INSERT OR REPLACE INTO comments (id, parent_id, created_at, subreddit, body, user, upvotes, downvotes) VALUES ("{id}", "{parent_id}", datetime("{created_at}", 'unixepoch'), "{subreddit}", "{body}", "{user}", "{upvotes}", "{downvotes}");"""
        sql_command = format_str.format(id = x['id'], parent_id = x['parent_id'], created_at = x['created_at'], subreddit = x['subreddit'], body = html.escape(x['body'], quote=True).encode('utf-8'), user = x['user'], upvotes = x['upvotes'], downvotes = x['downvotes'])
        cursor.execute(sql_command)
        connection.commit()
    
    else:
        Logger.log_level("Comment: DELETED", 3)




"""
Parses the HTML body of a Reddit comment for stream links (and performs an insert)
"""
def get_all(db) :

    connection = db['connection']
    cursor = db['cursor']

    comment_data = []

    # Execute query
    cursor.execute("SELECT * FROM comments") 

    # Fetch results
    # SQLite for python returns the records as a tuple without field names
    result = cursor.fetchall() 

    # Iterate through results and print them
    for r in result:

        comment_obj = map_db_record_to_object(r)

        comment_data.append(comment_obj)

    return comment_data



def map_db_record_to_object(r) :
    return {
        'id':         r[0], 
        'parent_id':  r[1], 
        'created_at': r[2], 
        'subreddit':  r[3], 
        'body':       html.unescape(r[4]),      
        'user':       r[5], 
        'upvotes':    r[6], 
        'downvotes':  r[7],            
    }


"""
Drop and create the comments table (for first-level comments to a Reddit post)
"""
def create_table(db) :

    connection = db['connection']
    cursor = db['cursor']
    
    # Create streams table
    cursor.execute('''DROP TABLE IF EXISTS comments''')
    
    cursor.execute('''CREATE TABLE comments (
        id text primary key not null, 
        parent_id text, 
        created_at datetime, 
        subreddit text, 
        body text,      
        user text, 
        upvotes real, 
        downvotes real,
        FOREIGN KEY(parent_id) REFERENCES submissions(id)
    )''')

    # Commit all the DB operations
    connection.commit()
