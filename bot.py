#!/usr/bin/python3
import praw
import pdb
import os

from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Create reddit instance and specify subreddit(s)
reddit = praw.Reddit(os.getenv("BOT_NAME"))
subreddit = reddit.subreddit(os.getenv("SUBREDDIT"))

# List sites and configs
sites = [
    ["tribunnews.com", "page=all"],
    ["kompas.com", "page=all"],
    ["detik.com", "single=1"]
]

# Check for post to reply
def post_matches(post, site, query):
    is_new = post.id not in replied_posts
    contains_site = site in post.domain
    contains_query = query in post.url
    return is_new and contains_site and not contains_query

# Create a list of replied posts
if not os.path.isfile("replied_posts.txt"):
    replied_posts = []
else:
    with open("replied_posts.txt", "r") as f:
        replied_posts = f.read()
        replied_posts = replied_posts.split("\n")
        replied_posts = list(filter(None, replied_posts))

# Format message
def message(url):
    message = "Here's a link to show all pages:\n\n"
    return message + url

# Send reply
def reply_post(post, query):
    newurl = urlparse(post.url)._replace(query=query).geturl()
    print(newurl)
    post.reply(message(newurl))

# Get the list of posts to reply to
for post in subreddit.new(limit=1):
    for site in sites:
        if post_matches(post, site[0], site[1]):
            reply_post(post, site[1])
            replied_posts.append(post.id)

# Write a list of replied posts into a file
with open("replied_posts.txt", "w") as f:
    for post_id in replied_posts:
        f.write(post_id + "\n")

