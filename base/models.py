from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    # Foreign Key is used for many to one relationships (many tasks to one user)
    # on_delete=models.CASCADE makes sure that if a user is deleted, all tasks under that user will also be deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True) # auto_now_add automatically tracks creation date

    def __str__(self):
        return self.title # The objects in Task will be represented as strings
    
    class Meta:
        ordering = ['complete'] # Makes it so tasks are ordered by completion status