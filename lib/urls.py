"""
    urls
"""

urls = (
    '/', 'IndexHandler',
    '/articles', 'ArticleHandler',
    '/articles/([\d]+)', 'ArticleHandler',
    '/signin', 'LoginHandler',
    '/editor', 'ManageHandler',
    '/timeline', 'TimelineHandler',
    '/rss.xml', 'RssHandler',
    '/tags/([\d]+)', 'TagHandler',
    '/search', 'SearchHandler',
    '/settings', 'SettingsHandler',
)
