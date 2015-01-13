import os

ROOT_DIR = os.path.abspath('.')
connect_str = 'sqlite:///{path}'.format(path=os.path.join(ROOT_DIR, 'pyprint.db3'))
cookie_secret = '3F8PhdGMSyuI5AjFM5Da8+/X2mP8XEzHtC/j57v3r6E='
