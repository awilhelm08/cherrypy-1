from cherrypy.test import test
test.prefer_parent_path()

import cherrypy
from cherrypy import tools


def setup_server():
    class Root:
        def index(self):
            yield "Hello, world"
        index.exposed = True
        h = [("Content-Language", "en-GB"), ('Content-Type', 'text/plain')]
        tools.response_headers(headers=h)(index)
        
        def other(self):
            return "salut"
        other.exposed = True
        other._cp_config = {
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [("Content-Language", "fr"),
                                               ('Content-Type', 'text/plain')],
            }
    
    cherrypy.tree.mount(Root())
    cherrypy.config.update({
            'log_to_screen': False,
            'environment': 'production',
    })


from cherrypy.test import helper

class ResponseHeadersTest(helper.CPWebCase):

    def testResponseHeadersDecorator(self):
        self.getPage('/')
        self.assertHeader("Content-Language", "en-GB")
        self.assertHeader('Content-Type', 'text/plain')

    def testResponseHeaders(self):
        self.getPage('/other')
        self.assertHeader("Content-Language", "fr")
        self.assertHeader('Content-Type', 'text/plain')

if __name__ == "__main__":
    setup_server()
    helper.testmain()
