from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Problem(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False, default='lowercase letters only')
    title = models.CharField(max_length=50, null=False, blank=False, default='')
    description = models.TextField()
    template = models.TextField(blank=False, default='')
    input = models.TextField(default='')
    correct_output = models.TextField(default='')

    def __str__(self):
        return self.name

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, default=1)
    code = models.TextField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    STATUS = [
        ("P", "Passed"),
        ("F", "Failed"),
    ]

    def __str__(self):
        return str(self.user.username) + ' ' + str(self.problem.name) + ' ' + str(self.date)