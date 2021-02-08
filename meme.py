import praw
import json
import logging

class meme:
    def __init__(self):
        try:
            with open("./configs/Reddit_conf.json") as h:
                reddit_creds = json.load(h)
        except FileNotFoundError as e:
            logging.error(e)
            raise e
        self.reddit = praw.Reddit(
            client_id=reddit_creds["client_id"],
            client_secret=reddit_creds["client_secret"],
            user_agent=reddit_creds["user_agent"],
            username=reddit_creds["username"],
            password=reddit_creds["password"]
        )
    def random(self):
        pass

    def is_logged(self):
        print(self.reddit.read_only())
