#
# encoding: utf-8
"""Test model module"""
from . import DBTestCase
from tornado.testing import gen_test
from torsche import Model, types
from torsche.query import MotorQuery


class TestModel(DBTestCase):
    """Test model"""

    @gen_test
    def test_should_have_objects(self):
        """Test if objects atribute returns the correct query object"""
        class MyModel(Model):
            pass
        query = MyModel.objects
        assert isinstance(query, MotorQuery)
        assert query._cls is MyModel


    @gen_test
    def test_should_query(self):
        """Teste de query do model"""
        class MyModel(Model):
            name = types.StringType(required=True)

        for i in xrange(10):
            self.sync_db.test_collection.insert({'name': 'test%s' % i})

        for index, instance in enumerate(MyModel.objects.find()):
            assert isinstance(instance, MyModel)
            assert instance.name == 'test%s' % index
