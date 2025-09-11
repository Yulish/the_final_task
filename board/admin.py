from django.contrib import admin
from .models import Category, Poster, Response
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

admin.site.register(Category)
admin.site.register(Poster)
admin.site.register(Response)

class PosterAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Poster
        fields = '__all__'


class PosterAdmin(admin.ModelAdmin):
    form = PosterAdminForm  # Используй форму с виджетом