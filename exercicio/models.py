import computed_property
from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError

ALTERADO_POR = "Alterado por"

ALTERADO_EM = "Alterado em"

CRIADO_POR = "Criado por"

CRIADO_EM = "Criado em"

"""
EXERRCÍCIOS ADMIN
"""


class Exercicio(models.Model):
    exe_descricao = models.TextField(verbose_name="Descrição")
    exe_criado_em = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=CRIADO_EM)
    exe_user_criado_por = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='exe_user_criado_por', verbose_name=CRIADO_POR)
    exe_alterado_em = models.DateTimeField(auto_now=True, verbose_name=ALTERADO_EM)
    exe_user_alterado_por = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, related_name='exe_user_alterado_por', verbose_name=ALTERADO_POR)

    def __str__(self):
        return self.exe_descricao


class ExercicioAlternativa(models.Model):
    eal_descricao = models.CharField(max_length=300, verbose_name='Alternativa')
    eal_eh_correta = models.BooleanField(default=False, verbose_name='Resposta correta?')
    eal_exercicio = models.ForeignKey(Exercicio, on_delete=models.PROTECT, verbose_name="Exercício")
    eal_criado_em = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Criado em")
    eal_user_criado_por = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='eal_user_criado_por', verbose_name="Criado por")
    eal_alterado_em = models.DateTimeField(auto_now=True, verbose_name="Alterado em")
    eal_user_alterado_por = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, related_name='eal_user_alterado_por', verbose_name="Alterado por")

    def __str__(self):
        return self.eal_descricao

    def clean(self):
        if self.eal_eh_correta and self.eal_exercicio:
            qtd = ExercicioAlternativa.objects.filter(
                eal_exercicio__id=self.eal_exercicio.id,
                eal_eh_correta=True
            ).count()
            if self.id and qtd > 1:
                raise ValidationError(
                    {'eal_eh_correta': 'Somente é possível ter uma alternativa correta por exercício!.'})
            elif not self.id and qtd != 0:
                raise ValidationError({'eal_eh_correta': 'Já há uma anternativa correta para ete exercício, '
                                                         'somente é permitida uma única alternativa marcada como correta!.'})
        super(ExercicioAlternativa, self).clean()

    def save(self, *args, **kwargs):
        super(ExercicioAlternativa, self).save(*args, **kwargs)


class UserEstatistica(models.Model):
    ues_qtd_exercicios_respondidos = computed_property.ComputedCharField(
        max_length=12, compute_from='qtd_exercicios_respondidos', editable=False,
        verbose_name='Quantidade de exercícios respondidos')
    ues_qtd_exercicios_totais = computed_property.ComputedCharField(
        max_length=12, compute_from='qtd_exercicios_totais', editable=False,
        verbose_name='Total de exercícios', default=0)
    ues_acertos = models.IntegerField(editable=False, default=0, verbose_name='Total de Acertos')
    ues_erros = models.IntegerField(editable=False, default=0, verbose_name='Total de Erros')
    ues_aproveitamento = computed_property.ComputedCharField(
        max_length=12, compute_from='aproveitamento', editable=False,
        verbose_name='Aproveitamento', default=0)
    ues_criado_em = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Criado em")
    ues_user_criado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ues_user_criado_por',
                                            verbose_name="Criado por", editable=False)
    ues_alterado_em = models.DateTimeField(auto_now=True, verbose_name="Alterado em")
    ues_user_alterado_por = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, related_name='ues_user_alterado_por', verbose_name="Alterado por",
        editable=False)

    @property
    def qtd_exercicios_respondidos(self):
        return self.ues_acertos + self.ues_erros

    @property
    def qtd_exercicios_totais(self):
        return Exercicio.objects.count()

    @property
    def aproveitamento(self):
        return int((self.ues_acertos * 100) / Exercicio.objects.count())


"""
EXERCICIOS CLIENTE
"""


class ExercicioResposta(models.Model):
    ere_exercicio = models.ForeignKey(Exercicio, on_delete=models.PROTECT, verbose_name='Exercício')
    ere_exercicioalternativa = models.ForeignKey(
        ExercicioAlternativa, on_delete=models.PROTECT, verbose_name='Alternativa Selecionada')
    ere_eh_alternativa_correta = models.BooleanField(default=False, verbose_name='Está correto?', editable=False)
    ere_criado_em = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Criado em")
    ere_user_criado_por = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='ere_user_criado_por', verbose_name="Criado por", editable=False)
    ere_alterado_em = models.DateTimeField(auto_now=True, verbose_name="Alterado em")
    ere_user_alterado_por = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, related_name='ere_user_alterado_por', verbose_name="Alterado por")

    def clean(self):
        if not self.id and self.exercicio:
            qtd = ExercicioResposta.objects.filter(
                exercicio__id=self.exercicio.id,
                ere_user_criado_por__id=self.ere_user_criado_por.id
            ).count()

            if qtd != 0:
                raise ValidationError('Você já respondeu a este exercício!')

        super(ExercicioResposta, self).clean()

    def save(self, *args, **kwargs):
        super(ExercicioResposta, self).save(*args, **kwargs)
