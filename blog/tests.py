from django.test import SimpleTestCase, Client
from django.views.generic import TemplateView
from . import views


class HomePageGetTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        url = '/'
        client = Client()
        cls.response = client.get(url)

    def test_url_access(self):
        self.assertEqual(type(self).response.status_code, 200)

    def test_url_name(self):
        self.assertEqual(type(self).response.resolver_match.url_name, 'home')

    def test_url_namespace(self):
        self.assertEqual(type(self).response.resolver_match.namespace, 'blog')

    def test_view_name(self):
        self.assertEqual(type(self).response.resolver_match.func, views.index)
    


class AboutPageGetTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        url = '/about/'
        client = Client()
        cls.response = client.get(url)
    
    def test_url_access(self):
        self.assertEqual(type(self).response.status_code, 200)

    def test_url_name(self):
        self.assertEqual(type(self).response.resolver_match.url_name, 'about')

    def test_url_namespace(self):
        self.assertEqual(type(self).response.resolver_match.namespace, 'blog')

    def test_view_name(self):
        self.assertEqual(type(self).response.resolver_match.func.view_class, TemplateView)


class ContactPageGetTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        url = '/contact/'
        client = Client()
        cls.response = client.get(url)

    def test_url_access(self):
        self.assertEqual(type(self).response.status_code, 302)

    def test_url_name(self):
        self.assertEqual(type(self).response.resolver_match.url_name, 'contact')

    def test_url_namespace(self):
        self.assertEqual(type(self).response.resolver_match.namespace, 'blog')

    def test_view_name(self):
        self.assertEqual(type(self).response.resolver_match.func, views.contact)
