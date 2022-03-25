import random
import string

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from exercicio.models import Exercicio


class ExercicioTestCase(APITestCase):

    def get_random_string(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username='admin', password=self.get_random_string(10))
        self.exercicio = Exercicio.objects.create(
            exe_descricao='teste 1', exe_user_criado_por=self.user)
        self.factory = APIClient()

    def test_exercicio(self):
        request = self.factory.get('/api/exercicio/', format='json')
        self.assertEqual(request.status_code, 200)
