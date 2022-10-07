from django.db import models
from django.db.models.fields import DateTimeField

class Subscribe(models.Model):
    email = models.EmailField()
    timestamp = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
