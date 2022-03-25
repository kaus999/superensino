import django_filters.rest_framework
from rest_framework import viewsets, mixins

from exercicio.models import Exercicio, ExercicioAlternativa, ExercicioResposta, UserEstatistica
from exercicio.serializers import ExercicioSerializer, ExercicioAlternativaSerializer, ExercicioRespostaSerializer, \
    UserEstatisticaSerializer


class ExercicioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lista de exercícios
    """
    queryset = Exercicio.objects.all()
    serializer_class = ExercicioSerializer


class ExercicioAlternativaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Alternativas dos exercícios
    """
    queryset = ExercicioAlternativa.objects.order_by('eal_criado_em').all()
    serializer_class = ExercicioAlternativaSerializer
    filter_fields = ['eal_exercicio__id']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


class ExercicioRespostaViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Respostas dos exercícios
    """
    queryset = ExercicioResposta.objects.all()
    serializer_class = ExercicioRespostaSerializer
    filter_fields = ['ere_user_criado_por__id']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]


class UserEstatisticaViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Estátisticas de respostas por usuário
    """
    queryset = UserEstatistica.objects.all()
    serializer_class = UserEstatisticaSerializer
    filter_fields = ['ues_user_criado_por__id']
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
