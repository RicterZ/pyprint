import re
from markdown import markdown as md


class Storage(dict):
    def __getattr__(self, item):
        return self[item]

    def __setattr__(self, key, value):
        self[key] = value


def get_host(url):
    return '/'.join(url.split('/')[2:-1])


def markdown(content):
    return md(content)


def fix_lazy_load(content):
    return re.sub(r'<img alt="(.+?)" src="" />', '<img src="\g<1>" />', content)

