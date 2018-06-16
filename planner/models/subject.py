from django.db import models

class Subject(models.Model):
    name = models.CharField(max_length=128, unique=True, db_index=True)
    color = models.PositiveSmallIntegerField(blank=True)

    def __str__(self):
        return self.name
