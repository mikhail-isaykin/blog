from django.db import models


class Classroom(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=11, unique=True)
    description = models.TextField(blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
