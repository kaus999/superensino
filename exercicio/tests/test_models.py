from django.contrib.auth.models import User
from django.test import TestCase

from exercicio.models import Exercicio, ExercicioAlternativa


class ExercicioTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='admin',
            password='adminadmin',
            email='admin@admin.com')
        self.exercicio = Exercicio.objects.create(
            exe_descricao='Pergunta Tests',
            exe_user_criado_por=self.user)

    def test_exercicio_create(self):
        self.exercicio = Exercicio.objects.create(
            exe_descricao='Pergunta Tests',
            exe_user_criado_por=self.user)
        self.assertIsNotNone(self.exercicio)

    def test_exercicio_alternativa_create(self):
        exercicio_alternativa = ExercicioAlternativa.objects.create(
            eal_exercicio_id=self.exercicio.id,
            eal_descricao='Alt1',
            eal_user_criado_por=self.user)
        self.assertIsNotNone(exercicio_alternativa)
