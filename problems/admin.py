from django.contrib import admin
from .models import Problem, Submission
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
# admin.site.register(Problem)

admin.site.register(Submission)


# Apply summernote to all TextField in model.
class SomeModelAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    # summernote_fields = '__all__'
    summernote_fields = ('description', 'constraints')

admin.site.register(Problem, SomeModelAdmin)