from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        result = super().clean()
        unique_tags = set()
        non_deleted_count = 0
        main_tags_count = 0
        for form in self.forms:
            if not form.cleaned_data:
                continue
            if form.cleaned_data.get('DELETE', False):
                continue
            if form.cleaned_data.get('is_main'):
                main_tags_count += 1
            non_deleted_count += 1
            unique_tags.add(form.cleaned_data['tag'])
        if non_deleted_count != len(unique_tags):
            raise ValidationError('Теги не должны повторяться')
        if main_tags_count == 0:
            raise ValidationError('Укажите основный раздел')
        if main_tags_count > 1:
            raise ValidationError('Основный раздел может быть только один')
        return result


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 0
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
