import re
from markdown import markdown


class Storage(dict):
    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value


def get_host(url):
    return '/'.join(url.split('/')[2:-1])


def posts_markdown(posts):
    if not isinstance(posts, (list,)):
        posts = [posts]

    return [Storage({
        'title': post.title,
        'created_time': post.created_time,
        'content': markdown(post.content),
        'tags': post.tags,
        'type': post.type,
    }) for post in posts]


def fix_lazy_load(posts):
    if not isinstance(posts, (list,)):
        posts = [posts]

    return [Storage({
        'title': post.title,
        'created_time': post.created_time,
        'content': re.sub(r'<img alt="(.+?)" src="" />', '<img src="\g<1>" />', post.content),
        'tags': post.tags
    }) for post in posts]

