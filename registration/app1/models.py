from django.db import models

# Create your models here.

class AccessRule(models.Model):
    is_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"Access Rule Enabled: {self.is_enabled}"
