from posts import ListPostsHandler, ListPostsByTagHandler, RetrievePostHandler, ArchiveHandler, FeedHandler
from links import ListLinksHandler
from others import AkarinHandler, NotFoundHandler
from background import SignInHandler, AddPostHandler, AddLinkHandler


handlers = [
    # posts.py
    (r'/', ListPostsHandler),
    (r'/page/([\d]+)?', ListPostsHandler),
    (r'/posts/(.*)', RetrievePostHandler),
    (r'/tags/(.*)', ListPostsByTagHandler),
    (r'/archives', ArchiveHandler),
    (r'/feed', FeedHandler),

    # links.py
    (r'/links', ListLinksHandler),

    # background
    (r'/login', SignInHandler),
    (r'/pyprint/add/post', AddPostHandler),
    (r'/pyprint/add/link', AddLinkHandler),

    # others.py
    (r'/akarin', AkarinHandler),
    (r'/(.*)', NotFoundHandler),
]