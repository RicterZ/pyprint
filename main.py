import tornado.ioloop
import tornado.httpserver
import tornado.options
from tornado.options import options, define

from pyprint import Application

define('port', default=8888, help='listen on the port', type=int)
define('address', default='0.0.0.0', help='binding at given address', type=str)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port, address=options.address)
    print '[+] PyPrint listening on {address}:{port}'.format(address=options.address,
        port=options.port)
    tornado.ioloop.IOLoop.instance().start()

