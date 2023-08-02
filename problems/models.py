from django.db import models

# Create your models here.
class Problem(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False, default='lowercase letters only')
    description = models.TextField()
    example = models.TextField(blank=True)
    constraints = models.TextField(blank=True)
    template = models.TextField(blank=False, default='')

    def __str__(self):
        return self.name