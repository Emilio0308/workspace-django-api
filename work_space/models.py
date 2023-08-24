from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class WorkSpace(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    created = models.DateTimeField(auto_now_add=True)
    menbers = models.ManyToManyField(User, related_name='workspaces')
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    done = models.BooleanField(default = False)
    status = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title