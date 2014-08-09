from posts import ListPostsHandler, ListPostsByTagHandler, RetrievePostHandler, ArchiveHandler
from links import ListLinksHandler
from others import AkarinHandler, NotFoundHandler


handlers = [
    # posts.py
    (r'/', ListPostsHandler),
    (r'/page/([\d]+)?', ListPostsHandler),
    (r'/posts/(.*)', RetrievePostHandler),
    (r'/tags/(.*)', ListPostsByTagHandler),
    (r'/archives', ArchiveHandler,),

    # links.py
    (r'/links', ListLinksHandler),

    # others.py
    (r'/akarin', AkarinHandler),
    (r'/(.*)', NotFoundHandler),
]