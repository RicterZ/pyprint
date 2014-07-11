"""
    urls
"""

urls = (
    '/', 'IndexHandler',
    '/articles', 'ArticleHandler',
    '/articles/([\d]+)', 'ArticleHandler',
    '/signin', 'LoginHandler',
    '/timeline', 'TimelineHandler',
    '/feed', 'RssHandler',
    '/tags/([\d]+)', 'TagHandler',
    '/search', 'SearchHandler',
    '/friends', 'FriendsHandler',
    '/editor', 'ManageHandler',
    '/editor/posts/([\d]+)', 'EditorHandler',
    '/editor/settings', 'SettingsHandler',
    '/editor/friends', 'FriendsManageHandler',
)

urls += (
    '/([\w\d-]+).html', 'PageHandler',
)
