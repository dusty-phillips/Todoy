from mongoengine import connect
from mongoengine.django.auth import User
from django.conf import settings
from django.test.client import Client
from django.test.utils import setup_test_environment

class MongoConnection:
    pass

def pytest_funcarg__mc(request):
    '''Funcarg for "mongoconnection" that should be used as the first argument
    in every test. mc has two variables, a mongoengine connection and a django
    test client. The database is destroyed after each test.'''
    test_db_name = settings.MONGO_DATABASE_NAME + "_test"
    setup_test_environment()
    connection = MongoConnection()
    connection.db = connect(test_db_name)
    connection.client = Client()
    connection.user = User.create_user("test_user", "test_user", "test_user@example.com")
    def dropdb():
        # Optimize: Might be quicker to delete collections
        connection.db.connection.drop_database(test_db_name)
    request.addfinalizer(dropdb)
    return connection
