#
# encoding: utf-8
from tornado import gen


class Manager(object):

    def __init__(self):
        pass

    def __get__(self, obj, objtype):

        return None


class MotorQuery(object):

    def __init__(self, cls, collection, io_loop):
        self.io_loop = io_loop
        self._cls = cls
        self._cursor = None
        self._query = None
        self._collection = collection

    def find(self, *args, **kwargs):
        self._query = self._collection.find(*args, **kwargs)
        return self

    def sort(self, *args, **kwargs):
        self._query = self._query.sort(*args, **kwargs)
        return self

    def __getitem__(self, index):
        return self._query[index]

    def _slice(self, start, stop):
        return self.limit(start - stop).skip(start)

    def limit(self, *args, **kwargs):
        self._query = self._query.limit(*args, **kwargs)
        return self

    def skip(self, *args, **kwargs):
        self._query = self._query.skip(*args, **kwargs)
        return self

    @gen.coroutine
    def fetch_next(self):
        res = yield self._query.fetch_next
        raise gen.Return(res)

    def next_object(self):
        obj = self._query.next_object()
        return self._cls(obj)

    def find_one(self, *args, **kwargs):
        res = self.io_loop.run_sync(self._query.find_one(*args, **kwargs))
        return self._cls(res)

    def __iter__(self):
        while self.io_loop.run_sync(self.fetch_next):
            yield self.next_object()
