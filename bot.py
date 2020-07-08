#!/usr/bin/python3
import praw
import pdb
import os

from pathlib import Path
from dotenv import load_dotenv

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

# Create a list of replied posts
if not os.path.isfile("replied_posts.txt"):
    replied_posts = []
else:
    with open("replied_posts.txt", "r") as f:
        replied_posts = f.read()
        replied_posts = replied_posts.split("\n")
        replied_posts = list(filter(None, replied_posts))

# Get the list of posts to reply to
for post in subreddit.new(limit=5):
    for site in sites:
        if post.id not in replied_posts and site[0] in post.domain and not site[1] in post.url:
            print(post.url + "?" + site[1])
            post.reply("Here's a link to show all pages:\n\n" + post.url + "?" + site[1])
            replied_posts.append(post.id)

# Write a list of replied posts into a file
with open("replied_posts.txt", "w") as f:
    for post_id in replied_posts:
        f.write(post_id + "\n")

