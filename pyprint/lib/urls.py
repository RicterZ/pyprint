urlpatterns = (
    '/', 'IndexHandler',
    '/page/([\d]+?)?', 'IndexHandler',
    '/posts/(.*)', 'PostHandler',
    '/tags/(.*)', 'TagHandler',
    '/archives', 'ArchivesHandler',
    '/links', 'LinkHandler',
    '/debug', 'DebugHandler',
    '/(.*)', 'NotFoundHandler',
)