from utils import Logger
from models import Comment

"""
Insert record into matches table
"""
def create(x, db) :

    connection = db['connection']
    cursor = db['cursor']

    # Build and execute SQL Insert query (uses new string interpolation method format() instead of % syntax)
    format_str = """INSERT OR REPLACE INTO submissions (id, created_at, subreddit, title, user, upvotes, downvotes, comment_count) VALUES ("{id}", datetime("{created_at}", 'unixepoch'), "{subreddit}", "{title}", "{user}", "{upvotes}", "{downvotes}", "{comment_count}");"""
    sql_command = format_str.format(id = x['id'], created_at = x['created_at'], subreddit = x['subreddit'], title = x['title'], user = x['user'], upvotes = x['upvotes'], downvotes = x['downvotes'], comment_count = x['comment_count'])
    cursor.execute(sql_command)
    connection.commit()

    Logger.log_level("Submission created: " + x['title'], 2)




"""
Store posts and comments from a subreddit in the DB tables 
"""
def create_with_comments(submissions_and_comments, db) :

    # Print all the submissions
    for s in submissions_and_comments:
        
        create(s, db)

        # You can get an unordered list of all comments flattened out with praw.helpers.flatten_tree(x.comments)
        for c in s['comments']:
            Comment.create(c, db)



"""
"""
def map_db_record_to_object(r) :
    
    return {
        'id':               r[0], 
        'created_at':       r[1],  
        'subreddit':        r[2], 
        'title':            r[3],     
        'user':             r[4], 
        'upvotes':          r[5], 
        'downvotes':        r[6],
        'comment_count':    r[7]          
    }




"""
Prints all matches in table
"""
def print_all(db) :

    connection = db['connection']
    cursor = db['cursor']

    # Execute query
    cursor.execute("SELECT * FROM submissions") 

    # Fetch results
    result = cursor.fetchall() 

    # Iterate through results and print them
    for r in result:
        result_dict = map_db_record_to_object(r)
        Logger.log_level("Submission: ", 1)
        Logger.log_level(result_dict['title'], 2)




"""
Drop and create the submissions table (for Reddit posts)
"""
def create_table(db) :

    connection = db['connection']
    cursor = db['cursor']
    
    cursor.execute('''DROP TABLE IF EXISTS submissions''')
    
    cursor.execute('''CREATE TABLE submissions (
        id text primary key not null, 
        created_at datetime, 
        subreddit text, 
        title text,
        user text, 
        upvotes real, 
        downvotes real, 
        comment_count real
    )''')

    # Commit all the DB operations
    connection.commit()


