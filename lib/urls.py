"""
    urls
"""

urls = (
    '/', 'IndexHandler',
    '/article', 'ArticleHandler',
    '/article/([\d]+)', 'ArticleHandler',
    '/signin', 'LoginHandler',
    '/editor', 'ManageHandler',
    '/timeline', 'TimelineHandler',
    '/rss.xml', 'RssHandler',
)
