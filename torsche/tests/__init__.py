#
# encoding: utf-8

from torsche import Connection
from tornado.testing import AsyncTestCase
from tornado.options import options


class DBTestCase(AsyncTestCase):

    def setUp(self):
        options.db = 'test'
        super(DBTestCase, self).setUp()
        Connection.set_io_loop(self.io_loop)
        self.db = Connection.get_connection()
        self.sync_db = self.db.connection.sync_client()[self.db.name]
        self.addCleanup(self.clean)

    def clean(self):
        Connection.drop()
        Connection.disconnect()


class TestDBTestCase(AsyncTestCase):

    def test_should_have_correct_io_loop(self):
        assert self.db._io_loop == self.io_loop
