from posts import ListPostsHandler, ListPostsByTagHandler, RetrievePostHandler, ArchiveHandler, FeedHandler
from links import ListLinksHandler
from others import AkarinHandler, NotFoundHandler, HitokotoHandler
from background import SignInHandler, ManagePostHandler, AddLinkHandler, AddPostHandler
from diaries import RetrieveDiaryHandler, ListDiariesHandler


handlers = [
    # posts.py
    (r'/', ListPostsHandler),
    (r'/page/([\d]+)?', ListPostsHandler),
    (r'/posts/(.*)', RetrievePostHandler),
    (r'/tags/(.*)', ListPostsByTagHandler),
    (r'/archives', ArchiveHandler),
    (r'/feed', FeedHandler),

    # diaries.py
    (r'/diaries', ListDiariesHandler),
    (r'/diaries/(.*)', RetrieveDiaryHandler),

    # links.py
    (r'/links', ListLinksHandler),

    # background
    (r'/login', SignInHandler),
    (r'/kamisama/posts', ManagePostHandler),
    (r'/kamisama/posts/add', AddPostHandler),
    (r'/kamisama/links', AddLinkHandler),

    # others.py
    (r'/akarin', AkarinHandler),
    (r'/hitokoto', HitokotoHandler),
    (r'/(.*)', NotFoundHandler),
]
