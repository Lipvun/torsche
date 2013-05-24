#
# encoding: utf-8

import motor
import tornado
from tornado.options import options, define
import os


class Connection(object):

    _database = None
    _client = None
    _is_configured = False

    @classmethod
    def set_io_loop(cls, io_loop):
        cls._io_loop = io_loop

    @classmethod
    def get_io_loop(cls):
        io_loop = getattr(cls, '_io_loop', None)
        if io_loop is None:
            io_loop = cls._io_loop = tornado.ioloop.IOLoop.instance()
        return io_loop

    @classmethod
    def get_client(cls):
        client = cls._client
        if not client:
            client = cls._client = cls.create_client()
        return client

    @classmethod
    def create_client(cls):
        return motor.MotorClient(host=cls._config['mongo_uri']).open_sync()

    @classmethod
    def _connect_db(cls, dbname):
        return cls.create_client()[dbname]

    @classmethod
    def get_connection(cls):
        if cls._database is None:
            if not cls._is_configured:
                cls.load_config()
            cls._database = cls._connect_db(cls._config['db'])
        return cls._database

    @classmethod
    def load_config(cls):
        cls._config = {}
        cls._config['mongo_uri'] = options.mongo_uri.format(**os.environ)
        cls._config['db'] = options.db
        cls._is_configured = True

    @classmethod
    def disconnect(cls):
        cls._database = None
        cls._client = None
        cls._is_configured = False

    @classmethod
    def drop(cls):
        db = cls.get_connection()
        db = db.connection.sync_client()[db.name]
        collection_names = db.collection_names()
        for collection_name in collection_names:
            if collection_name.startswith('system'):
                continue
            db[collection_name].drop()


def define_config():
    define('mongo_uri', default='mongodb://localhost', help='Mongo URI')
    define('db', default='feed', help='Mongo Database')


define_config()
