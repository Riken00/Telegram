from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class user_details(models.Model):
    number = models.IntegerField()
    api_id = models.CharField(max_length=9)
    api_hash = models.CharField(max_length=32)

    def __str__(self) :
        return str(self.number)
