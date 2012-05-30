#!/usr/bin/env python

import os,sys
import tornado
import tornado.ioloop
import tornado.web
import tornado.escape


class MainHandler(BaseHandler):
    def get(self):
        output =['Hello world!']
        output.append('by Tornado:'+ tornado.version)
        output.append('<a href="/env">Check Environment Variables</a>')
        output.append('<a href="/modules">Loaded Modules</a>')
        output.append('Python:'+sys.version)
        self.write('<br>'.join(output))

class EnvHandler(tornado.web.RequestHandler):
    def get(self):
        output =[]
        for item,value in os.environ.items():
            output.append('%s:%s'%(item,value))
        self.write('<br>'.join(output))

class ModulesHandler(tornado.web.RequestHandler):
    def get(self):
        output =[]
        for item,value in sys.modules.items():
            output.append('%s:%s'%(item,tornado.escape.xhtml_escape(str(value))))
        self.write('<br>'.join(output))

settings=dict(
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    xsrf_cookies=True,
    autoescape=None,
    debug=True,
)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/env", EnvHandler),
    (r"/modules", ModulesHandler),
],**settings)

def run(port='8080',address='127.0.0.1'):
    application.listen(port, address=address)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    run()
