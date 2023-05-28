from django.db import models

from django.db.models import JSONField

class Codeprofile(models.Model):
    submission_id = models.TextField()
    line = models.TextField()
    per_time = models.TextField()

    class Meta:
        db_table = "profiling_result"
