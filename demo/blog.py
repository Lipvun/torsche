#
# encoding: utf-8

import tornado.ioloop
from tornado.web import RequestHandler, Application, asynchronous
from tornado import gen
from torsche import Model, types
import  tornado.options


class Post(Model):
    text = types.StringType(required=True)


class MainHandler(RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):
        self.write("<html><body>")
        self.write('<form method="post">')
        self.write('<input type="text" name="text"/>')
        self.write('<input type="submit"/>')
        self.write('</form>')
        query = Post.objects.find()
        while (yield query.fetch_next()):
            post = query.next_object()
            self.write("<p>%s</p>" % post.text)
        self.write("</body></html>")

    @asynchronous
    @gen.coroutine
    def post(self):
        text = self.get_argument('text')
        post = Post(dict(text=text))
        yield post.save()
        self.redirect("/posts/")


application = Application([
    (r"/posts/", MainHandler),
], debug=True)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    tornado.options.print_help()
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
