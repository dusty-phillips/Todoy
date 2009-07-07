from django.test import TestCase

class SimpleTest(TestCase):
    def test_index_redirect(self):
        self.assertRedirects(self.client.get('/'), '/todos/', status_code=301)
