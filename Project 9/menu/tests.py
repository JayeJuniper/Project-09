from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
import datetime

from .models import Menu, Item, Ingredient
from .forms import MenuForm


# Portions of the following code have been compiled with aid by brianweber2 from Github.
# https://github.com/brianweber2
MENU_DATA = {
    'season': 'Summer',
    'expiration_date': '2018-03-20'
}


class MenuTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='Mayor',
            password='123456',
        )
        self.ingt1 = Ingredient.objects.create(name='lemon')
        self.ingt1.save()
        self.ingt2 = Ingredient.objects.create(name='lime')
        self.ingt2.save()
        self.ingt3 = Ingredient.objects.create(name='cane sugar')
        self.ingt3.save()
        self.ingt4 = Ingredient.objects.create(name='mountian spring mineral water')
        self.ingt4.save()
        self.item1 = Item.objects.create(
            name='lemon soda',
            description='''gently airated lemon baverage made from freshly juiced
             citrus, cane sugar and mountian spring mineral water.''',
            chef=self.user,
        )
        self.item1.save()
        self.item1.ingredients.add(self.ingt1, self.ingt3, self.ingt4)
        self.item2 = Item.objects.create(
            name='lime soda',
            description='''gently airated lime baverage made from freshly juiced citrus,
             cane sugar and mountian spring mineral water.''',
            chef=self.user,
        )
        self.item2.save()
        self.item2.ingredients.add(self.ingt2, self.ingt3, self.ingt4)
        self.menu = Menu.objects.create(season='spring 2020')
        self.menu.items.add(self.item1, self.item2)
        self.menu.save()

    def test_menu_list_view(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code,200)
        self.assertIn(self.menu, resp.context['menus'])
        self.assertTemplateUsed(resp, 'menu/menu_list.html')
        self.assertContains(resp, self.menu.season)

    def test_menu_detail_view(self):
        resp = self.client.get(reverse('menu_detail',
            kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')

    def test_create_new_menu_GET(self):
        resp = self.client.get(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)

    def test_create_new_menu_view_POST(self):
        resp = self.client.post(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)

    def test_edit_menu_GET(self):
        resp = self.client.get(reverse('menu_edit',
            kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_edit_menu_POST(self):
        resp = self.client.post(reverse('menu_edit',
            kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_item_detail_view(self):
        resp = self.client.get(reverse('item_detail',
            kwargs={'pk': self.item1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed('menu/detail_item.html')

    def test_item_view_404(self):
        resp = self.client.get(reverse('item_detail', 
            kwargs={'pk': 14}))
        self.assertEqual(resp.status_code, 404)
        self.assertTemplateUsed('menu/item_detail.html')

    def test_menu_create_form(self):
        form_data = {
            'season': 'Winter 2021',
            'items': [self.item1, self.item2],
            'expiration_date': '03/20/2023'
        }
        form = MenuForm(data=form_data)
        self.assertTrue(form.is_valid())
        menu = form.save()
        self.assertEqual(menu.season, 'Winter 2021')
        self.assertEqual(menu.expiration_date.date(), datetime.date(2023, 3, 20))
        self.assertEqual(menu.items.get(pk=self.item1.pk), self.item1)

    def test_menu_create_form_incomplete(self):
        form = MenuForm(data={})
        self.assertFalse(form.is_valid())

    def test_menu_creation(self):
        menu = Menu.objects.create(**MENU_DATA)
        self.assertEqual(menu.season, 'Summer')
