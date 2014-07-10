import markdown
import datetime
import hashlib
import random
import string


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


def json_format(item_list):
    if not item_list:
        return []
    keys = [key for key in item_list[0].__dict__.keys() if key not in ['_sa_instance_state']]
    return [dict(zip(keys, [item.__dict__[key] for key in keys])) for item in item_list]


def today():
    return datetime.datetime.date(datetime.datetime.today())


def password_to_md5(password):
    return hashlib.md5(password).hexdigest()


def make_session():
    return ''.join(random.sample(string.letters+string.digits, 20))



