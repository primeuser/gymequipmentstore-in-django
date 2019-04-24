from django.contrib import admin
from .models import *
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from django_summernote.admin import SummernoteModelAdmin


# Apply summernote to all TextField in model.
class SomeModelAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'


app_models = apps.get_app_config('gymapp').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass