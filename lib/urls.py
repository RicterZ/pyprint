urlpatterns = (
    '/', 'IndexHandler',
    '/posts/(.*)', 'PostHandler',
    '/tags/(.*)', 'TagHandler',
    '/links', 'LinkHandler',
    '/akarin', 'NotFoundHandler',
)