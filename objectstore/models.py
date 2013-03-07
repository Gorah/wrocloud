from django.db import models

class StoredObject(models.Model):
    user = models.CharField(max_length=200)
    url = models.URLField(max_length=1000)
