from django.db import models

class StoredObject(models.Model):
    container = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    url = models.URLField(max_length=1000)
    content_type = models.CharField(max_length=250)

class KeyValue(models.Model):
    storedobject = models.ForeignKey(
        StoredObject
    )
    key = models.CharField(max_length=250)
    value = models.TextField()

    def __unicode__(self):
        return "%s:%s" % (self.key, self.value)
