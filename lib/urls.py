"""
    urls
"""

urls = (
    '/', 'IndexHandler',
    '/articles', 'ArticleHandler',
    '/articles/([\d]+)', 'ArticleHandler',
    '/signin', 'LoginHandler',
    '/editor', 'ManageHandler',
    '/editor/friends', 'FriendLinkHandler',
    '/timeline', 'TimelineHandler',
    '/feed', 'RssHandler',
    '/tags/([\d]+)', 'TagHandler',
    '/search', 'SearchHandler',
    '/friends', 'FriendHandler',
)

urls += (
    '/([\w\d-]+).html', 'PageHandler',
)
