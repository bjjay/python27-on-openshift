#!/usr/bin/env python

import os,sys
import tornado
import tornado.ioloop
import tornado.web
import tornado.escape

from dropbox import client, rest, session

class AppConfig(object):
    def __init__(self):
        self.key = 'dk4w3ggzuh4aunw'
        self.secret = 'bajg7w3qwce0s33'
        self.type = 'app_folder'
        self.token = 'q32uw06poif5j7x|okcwi0b65furksy'

conf = AppConfig()

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self,application,request,**kwargs):
        self.sess = session.DropboxSession(conf.key, conf.secret, access_type=conf.type)
        self.sess.set_token(*conf.token.split('|'))
        self.client = client.DropboxClient(self.sess)
        self.base_path = ''
        tornado.web.RequestHandler.__init__(self,application,request,**kwargs)
    def decode(self,json):
        resp = {
            'parent':'..',
            'folders':[],
            'files':[],
            }
        if 'contents' in json:
            for f in json['contents']:
                f['path']=os.path.basename(f['path'])
                d = f['modified'][:-6]
                f['modified']=time.strftime('%Y-%m-%d %X',time.strptime(d,"%a, %d %b %Y %H:%M:%S"))
                if f['is_dir']:
                    f['size']='&lt;dir&gt;'
                    resp['folders'].append(f)
                else:
                    resp['files'].append(f)
        return  resp


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
