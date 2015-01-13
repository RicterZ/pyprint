import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import define, options
from pyprint import Application


define('port', default=8888, help='listen on the port', type=int)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()
