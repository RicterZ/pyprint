__author__ = 'Ricter'
import markdown
import datetime
import hashlib
import random
import string
from lib.settings import *


def render(template_file, title, **kwargs):
    return env.get_template(template_file).render(title=title, **kwargs)


def article_to_storage(data):
    """
    `data` is a `web.utils.IterBetter` instance
    """
    result_list = []
    for item in data:
        result_list.append(item)
    return result_list


def markdown_to_html(data):
    """
    `data` is a `web.utils.IterBetter` instance
    """
    result_list = []
    for item in data:
        item.content = markdown.markdown(item.content)
        result_list.append(item)
    return result_list


def clean_input(data):
    """Clean user input"""
    return data.replace('"', '').replace("'", '')


def now():
    return str(datetime.datetime.now()).split('.')[0]


def password_to_md5(password):
    return hashlib.md5(password).hexdigest()


def make_session():
    return ''.join(random.sample(string.letters+string.digits, 20))



