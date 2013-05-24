#
# encoding: utf-8
from . import DBTestCase
from tornado.testing import gen_test
from torsche.query import MotorQuery


class TestMotorQuery(DBTestCase):
    """Testes do MotorQuery"""
    @gen_test
    def test_should_query(self):
        """Teste de query do MotorQuery"""
        for i in xrange(10):
            self.sync_db.test_collection.insert({'name': 'test%s' % i})

        collection = self.db.test_collection
        query = MotorQuery(dict, collection, self.io_loop)
        query = query.find()
        cursor = self.sync_db.test_collection.find()
        assert list(query.find()) == list(cursor)

    # @gen_test
    # def test_should_slice(self):
    #     """query[start:stop]"""
    #     for i in xrange(10):
    #         self.sync_db.test_collection.insert({'name': 'test%s' % i})

    #     collection = self.db.test_collection
    #     query = MotorQuery(dict, collection, self.io_loop)
    #     query = query.find()[:5]
    #     result = []
    #     while (yield query.fetch_next()):
    #         result.append(query.next_object())
    #     cursor = self.sync_db.test_collection.find()
    #     assert result == list(cursor)[:5]

    # @gen_test
    # def test_should_get_by_index(self):
    #     """query[index]"""
    #     for i in xrange(10):
    #         self.sync_db.test_collection.insert({'name': 'test%s' % i})

    #     collection = self.db.test_collection
    #     query = MotorQuery(dict, collection, self.io_loop)
    #     result = yield query.find()[5]
    #     cursor = self.sync_db.test_collection.find()
    #     assert result == list(cursor)[5]
