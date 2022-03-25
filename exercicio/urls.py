from rest_framework import routers

from exercicio.apps import ExercicioConfig
from exercicio.views import ExercicioViewSet, ExercicioAlternativaViewSet, ExercicioRespostaViewSet, \
    UserEstatisticaViewSet

APP_NAME = ExercicioConfig.name

router = routers.DefaultRouter()
router.register('%s' % APP_NAME, ExercicioViewSet)
router.register('%s_alternativa' % APP_NAME, ExercicioAlternativaViewSet)
router.register('%s_resposta' % APP_NAME, ExercicioRespostaViewSet)
router.register('%s_resumo' % APP_NAME, UserEstatisticaViewSet)
