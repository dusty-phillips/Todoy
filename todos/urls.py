from django.conf.urls.defaults import *

urlpatterns = patterns('todoy.todos.views',
        url('/', 'day')
)

