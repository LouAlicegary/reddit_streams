from pprint import pprint
import praw
import html

import secrets
from utils import Logger


"""
Makes a connection to Reddit via PRAW 
"""
def connect() :

    # Create PRAW object
    r = praw.Reddit(user_agent='my_cool_application')

    # Log into Reddit
    r.login(secrets.reddit_username(), secrets.reddit_password(), disable_warning=True)

    return r



"""
"""
def scrape_posts(reddit_object, subreddit_name, post_limit) :

    submissions_list = []
    
    Logger.log_level("SUBREDDIT: " + subreddit_name, 1)

    subreddit = reddit_object.get_subreddit(subreddit_name)
    submissions = subreddit.get_new(limit = post_limit)

    for s in submissions:

        Logger.log_level("Scraping submission: " + s.title, 2)

        comments_list = []

        for c in s.comments:

            if c.author is not None:
                Logger.log_level("Scraping comment: posted by " + c.author.name, 3)
                comment_obj = {
                    'id':         c.name, 
                    'parent_id':  c.parent_id, 
                    'created_at': c.created_utc, 
                    'subreddit':  c.subreddit.display_name, 
                    'body':       html.unescape(c.body_html),      
                    'user':       c.author.name, 
                    'upvotes':    c.ups, 
                    'downvotes':  c.downs,            
                }
                comments_list.append(comment_obj)
            else:
                Logger.log_level("Scraping comment: Comment deleted.", 3)

        submission_obj = {
            'id': s.name,
            'created_at': s.created_utc,
            'subreddit': s.subreddit.display_name, 
            'title': s.title,
            'user': s.author.name, 
            'upvotes': s.ups, 
            'downvotes': s.downs, 
            'comment_count': s.num_comments,
            'comments': comments_list             
        }
        submissions_list.append(submission_obj)

    return submissions_list



"""
Pretty prints PRAW object data
"""
def print_praw_object(obj_type, obj) :

    str = "\n\n===========================\n*** {obj_type} object ***"
    Logger.log_level(str.format(obj_type = obj_type))
    pprint(vars(obj))
    Logger.log_level("======================================\n\n")    


"""
Returns a list of URLs scraped from the post
"""
def parse_urls_from_comment_body(body_html) :
    
    url_list = []

    link_list = body_html.split('<a href="')

    if len(link_list) > 1:
        for link in link_list[1:]:
            start_index = link.find("http")
            end_index = link.find('"')
            if start_index > -1 and end_index > -1:
                url_list.append(link[start_index:end_index])

    return url_list



"""
Parses the HTML body of a Reddit comment for stream links (and performs an insert)
"""
def parse_comments_for_streams(comment_data, db) :

    stream_list = []

    for comment in comment_data:

        url_list = parse_urls_from_comment_body(comment['body'])
        
        for url in url_list:
        
            stream_obj = {
                'url': url, 
                'source_type': "reddit", 
                'source_id': comment['id'],
                'provider': comment['user'], 
                'created_at': comment['created_at'], 
                'quality': "HD", 
                'language': "English",
                'rating': calculate_stream_rating(comment, url)
            }

            stream_list.append(stream_obj);

    return stream_list


def calculate_stream_rating(comment, url) :
    return comment['upvotes'] - comment['downvotes']

