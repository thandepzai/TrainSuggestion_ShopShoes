from django.db import models


class SessionList(models.Model):
    listCodeProduct = models.JSONField(null=False)
    status = models.BooleanField(default=True)
    objects = models.Manager()

    class Meta:
        db_table = 'SessionList'


class WordVector(models.Model):
    codeProduct = models.CharField(max_length=100, unique=True)
    vector = models.CharField(max_length=10000, unique=True)
    objects = models.Manager()

    def __str__(self):
        return self.codeProduct

    class Meta:
        db_table = 'WordVector'

