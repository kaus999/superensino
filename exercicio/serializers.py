from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from exercicio.models import Exercicio, ExercicioAlternativa, ExercicioResposta, UserEstatistica


class ExercicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercicio
        fields = '__all__'


class ExercicioAlternativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExercicioAlternativa
        fields = '__all__'


class ExercicioRespostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExercicioResposta
        fields = '__all__'

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if not hasattr(validated_data, 'ere_user_criado_por'):
            validated_data['ere_user_criado_por'] = user
        validated_data['ere_user_alterado_por'] = user

        alternativa = ExercicioAlternativa.objects.get(eal_exercicio__id=validated_data['ere_exercicio'].id,
                                                       id=validated_data['ere_exercicioalternativa'].id)
        validated_data['ere_eh_alternativa_correta'] = alternativa.eal_eh_correta

        if ExercicioResposta.objects.filter(
                ere_user_criado_por__id=user.id,
                ere_exercicio__id=validated_data['ere_exercicio'].id
        ).count() != 0:
            raise ValidationError({'detail': 'Você já respondeu a está pergunta!'})

        resposta = ExercicioResposta.objects.create(**validated_data)
        ExercicioRespostaSerializer.computar_resumo(alternativa, resposta, user)
        return resposta

    def computar_resumo(alternativa, resposta, user):
        """
        Verifica se deu certo a gravação da resposta, calcula se o usuário errou ou acertou e
        grava na tabela de userestatistica, para não necessitar recalcular toda vez que consulta o resumo
        """
        if resposta:
            try:
                resumo = UserEstatistica.objects.get(ues_user_criado_por__id=user.id)
                if alternativa.eal_eh_correta:
                    resumo.ues_acertos = resumo.ues_acertos + 1
                else:
                    resumo.ues_erros = resumo.ues_erros + 1
                resumo.save()
            except UserEstatistica.DoesNotExist:
                acertou = 0
                errou = 0
                if alternativa.eal_eh_correta:
                    acertou = 1
                else:
                    errou = 1
                UserEstatistica.objects.create(
                    ues_user_criado_por=user,
                    ues_user_alterado_por=user,
                    ues_erros=errou,
                    ues_acertos=acertou
                )


class UserEstatisticaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEstatistica
        fields = '__all__'
