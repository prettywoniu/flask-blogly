from app import app
from unittest import TestCase

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class BloglyTestCase(TestCase):
    """Test flask app"""

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)

#########???????????????????????############# 
### 1. if there is a redirect, what the status_code should be
### 2. Is it because of the redirection, the test could not pass
            
    def test_create_user(self):
        with app.test_client() as client:
            resp = client.post('/users/new', data={'first-name': 'Eva', 'last-name': 'Xu', 'img-url': ''})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertIn('Eva Xu', html)

    def test_delete(self):
        with app.test_client() as client:
            resp =  client.get('/users/4/delete')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn('Eva Xu', html)