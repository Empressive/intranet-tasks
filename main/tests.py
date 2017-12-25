import json

from django.test import TestCase, Client
from django.utils.encoding import force_text

from .models import ToDo


class CheckAPI(TestCase):
    fixtures = ['api.json']

    def setUp(self):
        self.client = Client()

    def test_post_method(self):
        response = self.client.post('/api/')

        self.assertEqual(response.status_code, 501)

    def test_get_method(self):
        response = self.client.get('/api/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(force_text(response.content))), ToDo.objects.count())

    def test_name_filter(self):
        response = self.client.get('/api/', {'name': 'First'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(force_text(response.content))[0]['id'], 1)

    def test_description_filter(self):
        response = self.client.get('/api/', {'description': 'row'})

        content = [row['id'] for row in json.loads(force_text(response.content))]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, [1, 2, 3, 4])

    def test_boolean_filter(self):
        response = self.client.get('/api/', {'is_done': 'True'})

        content = [row['id'] for row in json.loads(force_text(response.content))]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, [])

    def test_priority_filter(self):
        response = self.client.get('/api/', {'priority': 'High'})

        content = [row['id'] for row in json.loads(force_text(response.content))]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, [1])

    def test_parent_filter(self):
        response = self.client.get('/api/', {'parent': 'First'})

        content = [row['id'] for row in json.loads(force_text(response.content))]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, [2])

    def test_few_parameters_filter(self):
        response = self.client.get('/api/', {'parent': 'Second', 'description': 'row'})

        content = [row['id'] for row in json.loads(force_text(response.content))]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, [3, 4])
