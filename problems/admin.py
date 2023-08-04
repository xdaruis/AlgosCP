from django.contrib import admin
from .models import Problem, Submission
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
admin.site.register(Submission)

class SomeModelAdmin(SummernoteModelAdmin):
    summernote_fields = ('description', 'constraints')

admin.site.register(Problem, SomeModelAdmin)