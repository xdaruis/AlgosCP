from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Problem(models.Model):
    TIME_LIMIT_CHOICES = (
        (1, '1 second'),
        (2, '2 seconds'),
        (3, '3 seconds'),
        (5, '5 seconds'),
        (10, '10 seconds'),
        (15, '15 seconds'),
    )

    name = models.CharField(max_length=50, unique=True, null=False, blank=False, default='lowercase letters only')
    title = models.CharField(max_length=50, null=False, blank=False, default='')
    description = models.TextField()
    template = models.TextField(blank=False, default='')
    number_of_testcases = models.IntegerField(default=1)
    time_limit = models.IntegerField(choices=TIME_LIMIT_CHOICES, default=5)

    def __str__(self):
        return self.name

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, default=1)
    code = models.TextField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    test_cases = models.TextField(null=False, blank=False, default='')
    result = models.CharField(max_length=25, default='0')

    def __str__(self):
        return (
            f"#{self.pk} "
            f"{self.user.username} "
            f"{self.problem.name} "
            f"({self.date:%d-%m-%Y %H:%M})"
            )