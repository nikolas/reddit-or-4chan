#!/usr/bin/env python3
import random
import time
import requests

headers = {'User-Agent': 'Reddit or 4chan game, v0.1'}

reddit_url = 'https://www.reddit.com/r/linuxcirclejerk.json'
#fourchan_url = 'https://a.4cdn.org/s4s/thread/7358381.json'


# The sub-reddit has an array of children. Get a random one, then use
# its 'url' to look up a thread. The thread has data.children. Get a
# random one and return its selftext.
def get_reddit_comment():
    r = requests.get(reddit_url, headers=headers)
    print(r.json())

    return 'reddit'

# Get a random thread ID, then use it to get a random comment.
def get_fourchan_comment(board):
    fourchan_url = 'https://a.4cdn.org/{}/threads.json'.format(board)
    r = requests.get(fourchan_url, headers=headers)
    page = random.choice(r.json())
    thread = random.choice(page.get('threads'))
    thread_id = thread.get('no')

    thread_url = 'https://a.4cdn.org/{}/thread/{}.json'.format(board, thread_id)
    r = requests.get(thread_url, headers=headers)
    thread = r.json()

    # Now get a random post
    post = random.choice(thread.get('posts'))
    comment = post.get('com')

    return comment

# Get 10 random commands
def get_fourchan_comments(board):
    pass

def main():
    a = get_fourchan_comment('s4s')

    # sleep for three hours
    time.sleep(3600 * 3)

if __name__ == '__main__':
    while True:
        main()
