#
# encoding: utf-8
from . import Connection
from .query import MotorQuery
from schematics.models import Model as SchemaModel
from tornado import gen


class DBAccessor(object):

    def __get__(self, cls, owner):
        db = Connection.get_connection()
        return MotorQuery(owner, db['test_collection'], db.get_io_loop())

    def __set__(self, cls, value):
        raise Exception("You can't set objects")


class Model(SchemaModel):

    objects = DBAccessor()

    @gen.coroutine
    def save(self):
        res = yield self.objects.save(self.serialize())
        raise gen.Return(res)
