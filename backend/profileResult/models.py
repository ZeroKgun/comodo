from django.db import models

from django.db.models import JSONField

class Codeprofile(models.Model):
    submission_id = models.TextField()
    line = models.TextField()
    per_time = models.TextField()
    line_m = models.TextField(default ='')
    increment = models.TextField(default ='')

    class Meta:
        db_table = "profiling_result"
