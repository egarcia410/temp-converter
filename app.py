import os

import tornado.ioloop
import tornado.web

from jinja2 import Environment, PackageLoader, select_autoescape

PORT = int(os.environ.get('PORT', '8888'))

ENV = Environment(
    loader=PackageLoader('tempConvert'),
    autoescape=select_autoescape(['html', 'xml'])
)

class TemplateHandler(tornado.web.RequestHandler):
    def render_template (self, tpl, context={}):
        template = ENV.get_template(tpl)
        self.write(template.render(context))

class MainHandler(TemplateHandler):
    def get(self):
        self.set_header(
        'Cache-Control',
        'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("celsius.html")

    def post(self):
        self.set_header(
        'Cache-Control',
        'no-store, no-cache, must-revalidate, max-age=0')
        celsius = self.get_body_argument('celsius')
        if celsius == "":
            return self.render_template("celsius.html")
        fahrenheit = (float(celsius) * 1.8) + 32
        self.render_template("celsius.html", {'fahrenheit': round(fahrenheit, 2), 'celsius': celsius})

class FahrenheitHandler(TemplateHandler):
    def get(self):
        self.set_header(
        'Cache-Control',
        'no-store, no-cache, must-revalidate, max-age=0')
        self.render_template("fahrenheit.html")

    def post(self):
        self.set_header(
        'Cache-Control',
        'no-store, no-cache, must-revalidate, max-age=0')
        fahrenheit = self.get_body_argument('fahrenheit')
        if fahrenheit == "":
            return self.render_template("fahrenheit.html")
        celsius = round((((int(fahrenheit) - 32) * 5) / 9))
        self.render_template("fahrenheit.html", {'celsius': celsius, 'fahrenheit': fahrenheit})

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/fahrenheit", FahrenheitHandler),
        (
        r"/static/(.*)",
        tornado.web.StaticFileHandler,
        {'path': 'static'}
        )
    ], autoreload=True)

if __name__ == "__main__":
    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(PORT, print('Creating magic on port {}'.format(PORT)))
    tornado.ioloop.IOLoop.current().start()
