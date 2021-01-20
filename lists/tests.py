from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page


class SmokeTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_the_correct_url(self):
        responce = self.client.get('/')
        self.assertTemplateUsed(responce, 'home.html')
