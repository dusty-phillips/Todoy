from mongoengine import connect
from mongoengine.django.auth import User
from django.conf import settings, UserSettingsHolder
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
        connection.client.logout()
    request.addfinalizer(dropdb)
    return connection

# override_settings stolen from django 1.4
class OverrideSettingsHolder(UserSettingsHolder):
    """
    A custom setting holder that sends a signal upon change.
    """
    def __setattr__(self, name, value):
        UserSettingsHolder.__setattr__(self, name, value)
        #setting_changed.send(sender=self.__class__, setting=name, value=value)


class override_settings(object):
    """
    Acts as either a decorator, or a context manager. If it's a decorator it
    takes a function and returns a wrapped function. If it's a contextmanager
    it's used with the ``with`` statement. In either event entering/exiting
    are called before and after, respectively, the function/block is executed.
    """
    def __init__(self, **kwargs):
        self.options = kwargs
        self.wrapped = settings._wrapped

    def __enter__(self):
        self.enable()

    def __exit__(self, exc_type, exc_value, traceback):
        self.disable()

    def __call__(self, test_func):
        from django.test import TransactionTestCase
        if isinstance(test_func, type) and issubclass(test_func, TransactionTestCase):
            original_pre_setup = test_func._pre_setup
            original_post_teardown = test_func._post_teardown
            def _pre_setup(innerself):
                self.enable()
                original_pre_setup(innerself)
            def _post_teardown(innerself):
                original_post_teardown(innerself)
                self.disable()
            test_func._pre_setup = _pre_setup
            test_func._post_teardown = _post_teardown
            return test_func
        else:
            @wraps(test_func)
            def inner(*args, **kwargs):
                with self:
                    return test_func(*args, **kwargs)
        return inner

    def enable(self):
        override = OverrideSettingsHolder(settings._wrapped)
        for key, new_value in self.options.items():
            setattr(override, key, new_value)
        settings._wrapped = override

    def disable(self):
        settings._wrapped = self.wrapped
