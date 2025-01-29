from django.db import models

import sys
sys.path.append("..")

class Veterinary(models.Model):
    name = models.CharField(max_length=255, null=False)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False)
    image = models.ImageField(null=True, blank=True)


    def __str__(self):
        return self.name