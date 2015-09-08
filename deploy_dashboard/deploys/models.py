from django.db import models

class Release(models.Model):
    version = models.CharField(max_length=10)
    code_freeze_date = models.DateTimeField()
    production_release_date = models.DateTimeField()
    release_manager = models.CharField(max_length=200)
