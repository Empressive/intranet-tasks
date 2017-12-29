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

    def test_name_lowercase_filter(self):
        response = self.client.get('/api/', {'name': 'first'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(force_text(response.content))), 0)

    def test_description_filter(self):
        response = self.client.get('/api/', {'description': 'rOw'})

        content = [row['id'] for row in json.loads(force_text(response.content))]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, [1, 2, 3, 4])

    def test_wrong_description_filter(self):
        response = self.client.get('/api/', {'description': 'ro'})

        content = [row['id'] for row in json.loads(force_text(response.content))]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, [])

    def test_wrong_description_value_filter(self):
        response = self.client.get('/api/', {'description': 'This is'})

        self.assertContains(response, 'Value "This is" is not allowed for "description" field', status_code=400)

    def test_boolean_filter(self):
        response = self.client.get('/api/', {'is_done': 'True'})

        content = [row['id'] for row in json.loads(force_text(response.content))]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, [])

    def test_wrong_boolean_filter(self):
        response = self.client.get('/api/', {'is_done': 'Test'})

        self.assertContains(response, 'Value "Test" is not allowed for "is_done" field', status_code=400)

    def test_priority_filter(self):
        response = self.client.get('/api/', {'priority': 'High'})

        content = [row['id'] for row in json.loads(force_text(response.content))]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, [1])

    def test_wrong_priority(self):
        response = self.client.get('/api/', {'priority': 'Test'})

        self.assertContains(response, 'Value "Test" is not allowed for "priority" field', status_code=400)

    def test_parent_filter(self):
        response = self.client.get('/api/', {'parent': 'FiRsT'})

        content = [row['id'] for row in json.loads(force_text(response.content))]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, [2])

    def test_few_parameters_filter(self):
        response = self.client.get('/api/', {'parent': 'Second', 'description': 'row'})

        content = [row['id'] for row in json.loads(force_text(response.content))]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, [3, 4])

    def test_wrong_parameter(self):
        response = self.client.get('/api/', {'Wrong': 'Test'})

        self.assertContains(response, 'Parameter "Wrong" is not allowed for this method', status_code=400)
