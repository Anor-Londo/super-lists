from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item


class SmokeTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_the_correct_url(self):
        responce = self.client.get('/')
        self.assertTemplateUsed(responce, 'home.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_can_redirect_a_POST_request(self):
        responce = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(responce.status_code, 302)
        self.assertEqual(responce['location'], '/')

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.save()

        all_items = Item.objects.all()
        self.assertEqual(all_items.count(), 2)

        first_saved_item = all_items[0]
        second_saved_item = all_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'The second item')

class HomePageTest(TestCase):

    def test_only_save_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_display_all_list_items(self):
        Item.objects.create(text='Item_1')
        Item.objects.create(text='Item_2')

        responce = self.client.get('/')

        self.assertIn('Item_1', responce.content.decode())
        self.assertIn('Item_2', responce.content.decode())
