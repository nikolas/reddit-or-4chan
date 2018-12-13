#!/usr/bin/env python3
import bleach
import random
import time
import requests
import re
import html
import json


headers = {'User-Agent': 'Reddit or 4chan game, v0.1'}
reddit_subs = [
    'linuxcirclejerk', 'NoStupidQuestions', 'all',
    'cooking', '4chan', 'history', 'personalfinance',
    'travel',
]
fourchan_boards = [
    'b', 'g', 'pol', 's4s', 'ck', 'his', 'biz', 'trv',
]
quote_re = re.compile(r'>+(\d+)?(\s+)?')


def ignore_comment(comment):
    return 'reddit.com' in comment \
        or '/r/' in comment \
        or 'reddit' in comment \
        or re.match(r'r\/\w+', comment) \
        or 'thread' in comment \
        or 'board' in comment \
        or '/b/' in comment \
        or '/b' in comment


def clean_comment(comment):
    """Clean comment text for 4chan."""
    if comment is None:
        return ''

    # Decode HTML entities
    comment = html.unescape(comment)

    # Get rid of quote stuff
    comment = quote_re.sub('', comment)

    # Strip <a> tags
    comment = bleach.clean(
        comment,
        tags=[],
        strip=True,
        strip_comments=True
    )
    return comment


# Get all the comments in a comment tree. Reddit makes this so
# difficult compared to 4chan. There are some cool Redditors out there
# though. Like Pria.
def get_comments(thread):
    children = [e.get('data').get('children') for e in thread]

    comments = []

    for child in children:
        if len(child) < 1:
            continue

        # TODO: find nested comments here too
        comment = child[0].get('data').get('body')
        if comment:
            comments.append(comment)

    return comments


# The sub-reddit has an array of children. Get a random one, then use
# its 'url' to look up a thread. The thread has data.children. Get a
# random one and return its selftext.
def get_reddit_comment(sub):
    reddit_url = 'https://www.reddit.com/r/{}.json'.format(sub)
    r = requests.get(reddit_url, headers=headers)
    subreddit = r.json()
    thread = random.choice(subreddit.get('data').get('children'))
    thread_id = thread.get('data').get('id')
    thread_url = 'https://www.reddit.com/r/{}/comments/{}.json'.format(
        sub, thread_id)

    r = requests.get(thread_url, headers=headers)
    thread = r.json()

    # Find all nested comments
    comments = get_comments(thread)

    if comments:
        return random.choice(comments)

    return None


# Get a random thread ID, then use it to get a random comment.
def get_fourchan_comment(board):
    fourchan_url = 'https://a.4cdn.org/{}/threads.json'.format(board)
    r = requests.get(fourchan_url, headers=headers)
    page = random.choice(r.json())
    thread = random.choice(page.get('threads'))
    thread_id = thread.get('no')

    thread_url = 'https://a.4cdn.org/{}/thread/{}.json'.format(
        board, thread_id)
    r = requests.get(thread_url, headers=headers)
    thread = r.json()

    # Now get a random post
    post = random.choice(thread.get('posts'))
    comment = post.get('com')

    return comment


def get_reddit_comments():
    comments = []

    for i in range(30):
        sub = random.choice(reddit_subs)
        comment = get_reddit_comment(sub)
        if comment and not ignore_comment(comment):
            comments.append(comment)

    return comments


# Get 10 random comments
def get_fourchan_comments():
    comments = []

    for i in range(30):
        board = random.choice(fourchan_boards)
        comment = clean_comment(get_fourchan_comment(board))
        if comment and not ignore_comment(comment):
            comments.append(comment)

    return comments


def main():
    print('Browsing 4chan...')
    fourchan_comments = get_fourchan_comments()
    print('Browsing Reddit...')
    reddit_comments = get_reddit_comments()

    print('Writing to comments.txt')
    f = open('comments.txt', 'w')
    f.write(json.dumps({
        'fourchan': fourchan_comments,
        'reddit': reddit_comments,
    }))
    f.close()

    print('Waiting 3 hours.')
    time.sleep(3600 * 3)


if __name__ == '__main__':
    while True:
        main()
