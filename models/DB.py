import sqlite3

from models import DB, Submission, Comment, Stream
from utils import Logger


DB_NAME = "db/reddit_streams.db"



"""
"""
def initialize(rebuild = False) :

    # Create DB connection
    connection = sqlite3.connect(DB_NAME)

    # Get DB cursor
    cursor = connection.cursor()

    db = {
        'connection': connection,
        'cursor': cursor
    }

    if rebuild == True:
        Logger.log_level("Rebuilding tables.", 1)
        rebuild_tables(db)

    return db



"""
"""
def close(db) :
    db['connection'].close()



"""
Drop and re-create DB tables
"""
def rebuild_tables(db) :

    Submission.create_table(db)
    Comment.create_table(db)
    Stream.create_table(db)