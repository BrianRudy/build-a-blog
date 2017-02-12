import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Blogpost(db.Model):
    title = db.StringProperty(required = True)
    blogpost = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)

class Newpost(Handler):
    def render_newpost(self, title="", blogpost="", error=""):
        self.render("newpost.html", title=title, blogpost=blogpost, error=error)

    def get(self):
        self.render_newpost()

    def post(self):
        title = self.request.get("title")
        blogpost = self.request.get("blogpost")

        if title and blogpost:
            a = Blogpost(title = title, blogpost = blogpost)
            a.put()

            self.redirect("/blog")
        else:
            error = "we need both a title and a blogpost!"
            self.render_newpost(title, blogpost, error)

class Blog(Handler):
    def render_mainblog(self, title="", blogpost="", error=""):
        blogposts = db.GqlQuery("SELECT * FROM Blogpost ORDER BY created DESC LIMIT 5")

        self.render("mainblog.html", title=title, blogpost=blogpost, error=error, blogposts=blogposts)

    def get(self):
        title = self.request.get("title")
        blogpost = self.request.get("blogpost")
        self.render_mainblog()

    def post(self):
        self.redirect("/")

app = webapp2.WSGIApplication([
    ('/', Newpost),
    ('/blog', Blog)
], debug = True)
