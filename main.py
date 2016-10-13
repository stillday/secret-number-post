#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jinja2
import webapp2
import random

secret = random.randint(0, 100)
list = []

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

    def post(self):
        number = int(self.request.get("num"))

        if number == secret:
            self.write("Dein Tip war richtig. Folgende Zahlen hast du eingeben %s." % list)
            self.write(" Du hast %s versuche benötigt" % len(list))

        elif number < secret:
            self.write("Deine Tip war zu klein. Versuch es nochmal.")
            self.write(" Du hast bisher %s Versuche benötigt" % len(list))
            self.render_template("hello.html")

        else:
            self.write("Dein Tip war zu gross. Versuche es nochmal.")
            self.write(" Du hast bisher %s Versuche benötigt" % len(list))
            self.render_template("hello.html")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)
