#!/usr/bin/python3

import praw
import pdb
import os

from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse
from newspaper import Article

# Load env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Create reddit instance and specify subreddit(s)
bot = os.getenv("BOT_NAME")
reddit = praw.Reddit(bot)
subreddit = reddit.subreddit(os.getenv("SUBREDDIT"))

# List sites and configs
sites = [
    ["tribunnews.com", "page=all"],
    ["kompas.com", "page=all"],
    ["detik.com", "single=1"]
]

# STORAGE

# Create a list of replied posts or comments
def create_list(filename):
    if not os.path.isfile(filename):
        item = []
    else:
        with open(filename, "r") as f:
            item = f.read()
            item = item.split("\n")
            item = list(filter(None, item))
    return item

# Write a list of replied posts into files
def write_file(list, filename):
    with open(filename, "w") as f:
        for item in list:
            f.write(item + "\n")

# PAYLOAD

# Get url for the full page
def get_full_url(url, query):
    return urlparse(url)._replace(query=query).geturl()

# Get basic url
def get_url(url):
    for site in sites:
        if site[0] in urlparse(url).netloc:
            return get_full_url(url, site[1])
    return url

# Get formatted message
def get_message(url):
    message = "Here's a link to show all pages:\n\n"
    return message + url

# Get article text
def get_article(url):
    article = Article(get_url(url), 'id')
    article.download()
    article.parse()
    return article

# CHECKER

# Check post to reply
def check_post(post, site, query):
    is_new = post.id not in replied_posts
    contains_site = site in post.domain
    contains_query = query in post.url
    return is_new and contains_site and not contains_query

# Check comment to reply
def check_comment(comment):
    is_new = comment.id not in replied_comments
    contains_command = "!fulltext" in comment.body.lower()
    mentioned = "u/" + bot in comment.body
    return is_new and contains_command and mentioned

# REPLY

# Send reply to post
def reply_post(post, query):
    url = get_full_url(post.url, query)
    post.reply(get_message(url))

# Send reply to comment
def reply_comment(comment):
    article = get_article(comment.submission.url)
    if article.text:
        title = "**" + article.title + "**"
        comment.reply(title + "\n\n" + article.text)
    else:
        comment.reply("Sorry, can't seem to get the full text of this article..")

# MAIN

# Create a list of replied posts and comments
replied_posts = create_list("replied_posts.txt")
replied_comments = create_list("replied_comments.txt")

# Get the list of posts to reply to
for post in subreddit.new(limit=5):
    for site in sites:
        if check_post(post, site[0], site[1]):
            print("post: " + post.id)
            reply_post(post, site[1])
            replied_posts.append(post.id)

# Get the list of comments to reply to
for comment in subreddit.comments(limit=10):
    if check_comment(comment):
        print("comment: " + comment.id)
        reply_comment(comment)
        replied_comments.append(comment.id)

# Write the list of replied posts and comments into files
write_file(replied_posts, "replied_posts.txt")
write_file(replied_comments, "replied_comments.txt")

# END

