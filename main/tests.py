import json

from django.test import TestCase, Client
from django.utils.encoding import force_text

from .models import ToDo
from .constants import PRIORITY_CHOICES


class CheckAPI(TestCase):
    def setUp(self):
        self.client = Client()

        ToDo(name='First', description='This is first row', is_done=False, priority='High', parent=None).save()
        ToDo(name='Second', description='This is second row', is_done=True, priority='Low', parent_id=1).save()
        ToDo(name='Third', description='This is third row', is_done=True, priority='Normal', parent_id=1).save()

    def test_PostMethod(self):
        response = self.client.post('/api/')

        self.assertEqual(response.status_code, 405)

    def test_GetMethod(self):
        response = self.client.get('/api/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(force_text(response.content))), ToDo.objects.count())

    def test_FilterName(self, name='First'):
        todo = ToDo.objects
        response = self.client.get('/api/', {'name': name})

        if not name:
            todo = todo.all()
        else:
            todo = todo.filter(name=name).values()

        right_response = []

        for row in todo:
            right_response.append(row)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(force_text(response.content), json.dumps(right_response))

    def test_FilterContains(self, description='row'):
        todo = ToDo.objects
        response = self.client.get('/api/', {'description': description})

        if not description:
            todo = todo.all().values()
        else:
            todo = todo.filter(description__icontains='row').values()

        right_response = []

        for row in todo:
            right_response.append(row)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(force_text(response.content), json.dumps(right_response))

    def test_FilterBoolean(self, is_done='True'):
        todo = ToDo.objects
        response = self.client.get('/api/', {'is_done': is_done})

        if not str(is_done):
            todo = todo.all().values()
        else:
            if is_done not in ['True', 'true', '1', '0', 'false', 'False']:
                return self.assertEqual(response.status_code, 400)

            if is_done in ['True', 'true', '1']:
                is_done = 1
            else:
                is_done = 0

            todo = todo.filter(is_done=is_done).values()

        right_response = []

        for row in todo:
            right_response.append(row)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(force_text(response.content), json.dumps(right_response))

    def test_FilterPriority(self, priority='High'):
        todo = ToDo.objects
        response = self.client.get('/api/', {'priority': priority})

        if not priority:
            todo = todo.all().values()
        else:
            if (priority, priority) not in PRIORITY_CHOICES:
                return self.assertEqual(response.status_code, 400)

            todo = todo.filter(priority=priority).values()

        right_response = []

        for row in todo:
            right_response.append(row)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(force_text(response.content), json.dumps(right_response))

    def test_FilterParentName(self, parent_name='First'):
        response = self.client.get('/api/', {'parent': parent_name})

        todo = ToDo.objects.filter(parent__name__icontains=parent_name).values()
        right_response = []

        for row in todo:
            right_response.append(row)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(force_text(response.content), json.dumps(right_response))

    def test_FilterFewParameters(self):
        params = {'parent': 'First', 'description': 'row'}

        response = self.client.get('/api/', params)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(force_text(response.content))), 2)
