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

# Get formatted message
def get_message(url):
    message = "Here's a link to show all pages:\n\n"
    return message + url

# CHECKER

# Check post to reply
def check_post(post, site, query):
    is_new = post.id not in replied_posts
    contains_site = site in post.domain
    contains_query = query in post.url
    return is_new and contains_site and not contains_query

# REPLY

# Send reply to post
def reply_post(post, query):
    url = get_full_url(post.url, query)
    post.reply(get_message(url))

# MAIN

# Create a list of replied posts and comments
replied_posts = create_list("replied_posts.txt")

# Get the list of posts to reply to
for post in subreddit.new(limit=5):
    for site in sites:
        if check_post(post, site[0], site[1]):
            print("post: " + post.id)
            reply_post(post, site[1])
            replied_posts.append(post.id)

# Write the list of replied posts and comments into files
write_file(replied_posts, "replied_posts.txt")

# END

