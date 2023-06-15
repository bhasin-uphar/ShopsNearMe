from django.test import TestCase, Client
from django.urls import reverse
from .models import Shop

class ShopViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.shop = Shop.objects.create(name='Example Shop', latitude=0.0, longitude=0.0)

    def test_shop_list_view(self):
        response = self.client.get(reverse('shop_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.shop.name)

    def test_shop_detail_view(self):
        response = self.client.get(reverse('shop_detail', args=[self.shop.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.shop.name)

    def test_shop_create_view(self):
        response = self.client.post(reverse('shop_create'), {'name': 'New Shop', 'latitude': 1.0, 'longitude': 1.0})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Shop.objects.count(), 2)
        new_shop = Shop.objects.latest('id')
        self.assertRedirects(response, reverse('shop_detail', args=[new_shop.id]))

    def test_shop_update_view(self):
        response = self.client.post(reverse('shop_update', args=[self.shop.id]), {'name': 'Updated Shop', 'latitude': 2.0, 'longitude': 2.0})
        self.assertEqual(response.status_code, 302)
        updated_shop = Shop.objects.get(id=self.shop.id)
        self.assertEqual(updated_shop.name, 'Updated Shop')
        self.assertEqual(updated_shop.latitude, 2.0)
        self.assertEqual(updated_shop.longitude, 2.0)

    def test_shop_within_distance_view(self):
        response = self.client.post(reverse('shop_within_distance'), {'latitude': 0.0, 'longitude': 0.0, 'distance': 1.0})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.shop.name)

        response = self.client.post(reverse('shop_within_distance'), {'latitude': 2.0, 'longitude': 0.0, 'distance': 0.5})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.shop.name)
