from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from collections import OrderedDict


class AllTasksTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/api/signup/',
                         {'username': 'qwerty', 'password': 'password'})
        response = self.client.post(
            '/api/login/', {'username': 'qwerty', 'password': 'password'})
        self.token = 'Token {0}'.format(response.data['token'])

    def test_no_data(self):
        response = self.client.get('/api/all/', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.data, [])

    def test_invalid_credentials(self):
        response = self.client.get(
            '/api/all/', HTTP_AUTHORIZATION='{0}{1}'.format(self.token, 'test'))
        self.assertEqual(response.data['detail'], 'Invalid token.')

    def test_one_task(self):
        self.client.post(
            '/api/new/', {'title': 'test', 'description': 'test-d',
                          'status': 'new', 'completion': '2020-10-10T18:00'},
            HTTP_AUTHORIZATION=self.token)
        response = self.client.get(
            '/api/all/', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(len(response.data), 1)

    def test_two_tasks(self):
        self.client.post(
            '/api/new/', {'title': 'test', 'description': 'test-d',
                          'status': 'new', 'completion': '2020-10-10T18:00'},
            HTTP_AUTHORIZATION=self.token)
        self.client.post(
            '/api/new/', {'title': 'test-1', 'description': 'test-d-1',
                          'status': 'planned', 'completion': '2020-12-10T18:00'},
            HTTP_AUTHORIZATION=self.token)
        response = self.client.get(
            '/api/all/', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(len(response.data), 2)


class GUDTasksTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/api/signup/',
                         {'username': 'qwerty', 'password': 'password'})
        response = self.client.post(
            '/api/login/', {'username': 'qwerty', 'password': 'password'})
        self.token = 'Token {0}'.format(response.data['token'])

    def test_get_task(self):
        url = self.client.post(
            '/api/new/', {'title': 'test', 'description': 'test-d',
                          'status': 'new', 'completion': '2020-10-10T18:00'},
            HTTP_AUTHORIZATION=self.token).data['URL']
        response = self.client.get(
            url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.data['title'], 'test')
        self.assertEqual(response.data['description'], 'test-d')
        self.assertEqual(response.data['status'], 'new')
        self.assertEqual(response.data['completion'], '2020-10-10T18:00:00Z')

    def test_delete_task(self):
        url = self.client.post(
            '/api/new/', {'title': 'test', 'description': 'test-d',
                          'status': 'new', 'completion': '2020-10-10T18:00'},
            HTTP_AUTHORIZATION=self.token).data['URL']
        response = self.client.delete(
            url, HTTP_AUTHORIZATION=self.token)
        self.assertTrue(response.data['done'])

    def test_update_task(self):
        url = self.client.post(
            '/api/new/', {'title': 'test', 'description': 'test-d',
                          'status': 'new', 'completion': '2020-10-10T18:00'},
            HTTP_AUTHORIZATION=self.token).data['URL']
        response = self.client.put(
            url, {'title': 'test-u'}, HTTP_AUTHORIZATION=self.token, content_type='application/json')
        response_get_task = self.client.get(
            url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.data['title'], 'test -> test-u')
        self.assertEqual(response_get_task.data['title'], 'test-u')

    def test_update_wrong_status(self):
        url = self.client.post(
            '/api/new/', {'title': 'test', 'description': 'test-d',
                          'status': 'new', 'completion': '2020-10-10T18:00'},
            HTTP_AUTHORIZATION=self.token).data['URL']
        response = self.client.put(
            url, {'status': 'weird'}, HTTP_AUTHORIZATION=self.token, content_type='application/json')
        response_get_task = self.client.get(
            url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.data['status'],
                         'empty/invalid format/the same data')
        self.assertEqual(response_get_task.data['status'], 'new')

    def test_changing_several_fields(self):
        url = self.client.post(
            '/api/new/', {'title': 'test', 'description': 'test-d',
                          'status': 'new', 'completion': '2020-10-10T18:00'},
            HTTP_AUTHORIZATION=self.token).data['URL']
        response = self.client.put(url,
                                   {'description': 'test-d-u',
                                    'status': 'done',
                                    'completion': '2020-11-21T12:00', },
                                   HTTP_AUTHORIZATION=self.token,
                                   content_type='application/json')
        response_get_task = self.client.get(
            url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response_get_task.data['description'], 'test-d-u')
        self.assertEqual(response_get_task.data['status'], 'done')
        self.assertEqual(
            response_get_task.data['completion'], '2020-11-21T12:00:00Z')


class GetTaskChangesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post('/api/signup/',
                         {'username': 'qwerty', 'password': 'password'})
        response = self.client.post(
            '/api/login/', {'username': 'qwerty', 'password': 'password'})
        self.token = 'Token {0}'.format(response.data['token'])

    def test_changing_1_time(self):
        url = self.client.post(
            '/api/new/', {'title': 'test', 'description': 'test-d',
                          'status': 'new', 'completion': '2020-10-10T18:00'},
            HTTP_AUTHORIZATION=self.token).data['URL']
        response = self.client.put(url,
                                   {'description': 'test-d-u'},
                                   HTTP_AUTHORIZATION=self.token,
                                   content_type='application/json')
        response_get_task_changes = self.client.get(
            '{0}/{1}'.format(url, 'changes'), HTTP_AUTHORIZATION=self.token)
        self.assertEqual(len(response_get_task_changes.data), 1)
        changes_set = response_get_task_changes.data[0]
        self.assertEqual(
            changes_set['changed_title'], 'No changes.')
        self.assertEqual(
            changes_set['changed_description'], 'test-d -> test-d-u')
        self.assertEqual(
            changes_set['changed_status'], 'No changes.')
        self.assertEqual(
            changes_set['changed_completion'], 'No changes.')
