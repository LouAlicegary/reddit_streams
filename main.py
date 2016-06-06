from models import DB, Submission, Comment, Stream
from services import Reddit
from utils import Logger


def main() :

    POST_LIMIT = 10
    STREAMING_SUBS = ['mlbstreams', 'nbastreams', 'soccerstreams'] #, 'nflstreams', 'nhlstreams', 'cfbstreams', 'ncaabballstreams', 'boxingstreams', 'mmastreams']
    
    db = DB.initialize(rebuild = False);

    # Connect to Reddit
    reddit_obj = Reddit.connect()

    # Create submissions and comments
    for sub in STREAMING_SUBS:
        submissions_with_comments = Reddit.scrape_posts(reddit_obj, sub, POST_LIMIT)
        Submission.create_with_comments(submissions_with_comments, db)
    
    # Parse comments for streams
    comment_data = Comment.get_all(db)
    stream_list = Reddit.parse_comments_for_streams(comment_data, db)
    
    # Create streams
    for stream in stream_list:
        Stream.create(stream, db)

    # Print the matches table from SQLite
    Submission.print_all(db)

    # Close the DB connection
    DB.close(db)


main()
