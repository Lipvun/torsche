#
# encoding: utf-8
from torsche import Connection
from tornado.testing import AsyncTestCase, gen_test
from tornado.options import options
import mock
import os


class TestConnection(AsyncTestCase):

    def setUp(self):
        super(TestConnection, self).setUp()
        self._reset_config()
        Connection.set_io_loop(self.io_loop)
        self.addCleanup(self.clean)

    def tearDown(self):
        super(TestConnection, self).tearDown()
        Connection.disconnect()

    def test_should_connect(self):
        db = Connection.get_connection()
        assert db.name == 'test'

    def test_should_use_mongo_uri(self):
        options.mongo_uri = 'mycrazy://uri'
        Connection.load_config()
        with mock.patch('motor.MotorClient') as MockMotorClient:
            MockMotorClient.return_value.open_sync.return_value = 'my'
            assert Connection.create_client() == 'my'
            MockMotorClient.assert_called_with(host='mycrazy://uri')

    def test_should_compose_uri_with_environ(self):
        options.mongo_uri = 'mycrazy://{GLB_FEED_MONGO_USR}:{GLB_FEED_MONGO_PWD}@localhost'
        os.environ['GLB_FEED_MONGO_USR'] = 'fakeuser'
        os.environ['GLB_FEED_MONGO_PWD'] = 'fakepass'
        Connection.load_config()
        assert Connection._config['mongo_uri'] == 'mycrazy://fakeuser:fakepass@localhost'

    @gen_test
    def test_should_drop(self):
        db = Connection.get_connection()
        collection = db.test_collection
        result = yield collection.insert({'name': 'test'})
        result = yield collection.count()
        assert result == 1
        #TODO: Isso deveria funcionar assim: Connection.drop()
        yield db.test_collection.drop()
        collection = db.test_collection
        result2 = yield collection.count()
        assert result2 == 0

    def clean(self):
        Connection.disconnect()
        self._reset_config()
        self._drop_test_collection()
        Connection.disconnect()

    def _reset_config(self):
        options.db = 'test'
        options.mongo_uri = 'mongodb://localhost'
        Connection.load_config()

    def _drop_test_collection(self):
        db = Connection.get_connection()
        sync_db = db.connection.sync_client()[db.name]  # pega client sync
        sync_db.test_collection.drop()
