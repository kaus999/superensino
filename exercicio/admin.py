from django.contrib import admin

from exercicio.models import Exercicio, ExercicioAlternativa, UserEstatistica


class ReadOnlyAdminMixin:
    readonly_fields = []

    actions = None
    list_display_links = None

    def change_view(self, request, object_id, extra_context=None):
        """ customize add/edit form to remove save / save and continue """
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super().change_view(request, object_id, extra_context=extra_context)

    def has_add_permission(self, request):
        return False

    def has_change_permission(selfself, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(ReadOnlyAdminMixin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        pass

    def delete_model(self, request, obj):
        pass

    def save_related(self, request, form, formsets, change):
        pass


class ExercicioAlternativaInline(admin.TabularInline):
    """
    Inline alternativas para os exercícios no admin
    """
    line_numbering = 0
    fields = ('eal_descricao', 'eal_eh_correta')
    model = ExercicioAlternativa
    extra = 4
    create_from_default = True
    max_num = 4

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if not hasattr(instance, 'eal_user_criado_por'):
            instance.eal_user_criado_por = request.user
        instance.eal_user_alterado_por = request.user
        instance.save()
        form.save_m2m()
        return instance

    def save_formset(self, request, form, formset, change):

        def set_user(instance):
            if not instance.eal_user_criado_por:
                instance.eal_user_criado_por = request.user
            instance.eal_user_alterado_por = request.user
            instance.save()

        if formset.model == ExercicioAlternativa:
            instances = formset.save(commit=False)
            map(set_user, instances)
            formset.save_m2m()
            return instances
        else:
            return formset.save()


class ExercicioAdmin(admin.ModelAdmin):
    """
    Exercícios no admin
    """
    fields = ['exe_descricao']
    inlines = [ExercicioAlternativaInline]

    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # jquery
            'exercicio/js/exercicio.js',  # static folder
        )

    def save_model(self, request, obj, form, change):
        exercicio = form.save(commit=False)
        if exercicio and not hasattr(exercicio, 'exe_user_criado_por'):
            exercicio.exe_user_criado_por = request.user
        exercicio.exe_user_alterado_por = request.user
        exercicio.save()
        form.save_m2m()
        return exercicio

    def save_formset(self, request, form, formset, change):

        def set_user(exercicio: Exercicio):
            if exercicio and not exercicio.exe_user_criado_por_id:
                exercicio.exe_user_criado_por_id = request.user.id
            exercicio.exe_user_alterado_por_id = request.user.id
            exercicio.save()

        def set_user_alternativa(alternativa: ExercicioAlternativa):
            if alternativa and not alternativa.eal_user_criado_por_id:
                alternativa.eal_user_criado_por_id = request.user.id
            alternativa.eal_user_alterado_por_id = request.user.id
            alternativa.save()

        if formset.model == Exercicio:
            instances = formset.save(commit=False)
            for instance in instances:
                set_user(instance)
            formset.save_m2m()
            return instances
        elif formset.model == ExercicioAlternativa:
            instances = formset.save(commit=False)
            for instance in instances:
                set_user_alternativa(instance)
            formset.save_m2m()
            return instances
        else:
            return formset.save()


class UserEstatisticaAdminMixin(ReadOnlyAdminMixin, admin.ModelAdmin):
    readonly_fields = (
        'ues_user_criado_por',
        'ues_qtd_exercicios_respondidos',
        'ues_acertos',
        'ues_erros')
    actions = None
    list_display_links = None


admin.site.register(Exercicio, ExercicioAdmin)
admin.site.register(UserEstatistica)
