import re
from markdown import markdown


def get_host(url):
    return '/'.join(url.split('/')[2:-1])


def posts_markdown(posts):
    if not isinstance(posts, (list,)):
        posts = [posts]

    return [{
        'title': post.title,
        'created_time': post.created_time,
        'content': markdown(post.content),
        'tags': post.tags
    } for post in posts]


def lazy_load(posts):
    pass