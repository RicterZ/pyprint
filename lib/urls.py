urlpatterns = (
    '/', 'IndexHandler',
    '/posts/(.*)', 'PostHandler',
    '/tags/(.*)', 'TagHandler',
    '/links', 'LinkHandler',
    '/test', 'TestHandler',
    '/(.*)', 'NotFoundHandler',
)