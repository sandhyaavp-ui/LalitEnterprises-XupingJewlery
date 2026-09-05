import json

from django import forms
from django.contrib import admin

from .models import Collection, Product


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'default_moq')
    list_editable = ('default_moq',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    class Media:
        js = ('catalog/admin_moq_autofill.js',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    change_form_template = 'admin/catalog/product/change_form.html'
    list_display = ('name', 'collection', 'moq', 'created_at')
    list_filter = ('collection',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['collection_moq_map'] = json.dumps(
            {str(c.pk): c.default_moq for c in Collection.objects.all()}
        )
        return super().changeform_view(request, object_id, form_url, extra_context)
