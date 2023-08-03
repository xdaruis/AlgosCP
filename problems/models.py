from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Problem(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False, default='lowercase letters only')
    description = models.TextField()
    example = models.TextField(blank=True)
    constraints = models.TextField(blank=True)
    template = models.TextField(blank=False, default='')

    def __str__(self):
        return self.name

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, default=1)
    code = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    STATUS = [
        ("P", "Passed"),
        ("F", "Failed"),
    ]

    def __str__(self):
        return str(self.user.username) + ' ' + str(self.problem.name)