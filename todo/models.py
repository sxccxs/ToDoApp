from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    text = models.CharField(max_length=150, verbose_name='Text')
    is_completed = models.BooleanField(default=False, verbose_name='Is Completed')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Created By')
    
    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created']
    
    def __str__(self):
        return self.text
