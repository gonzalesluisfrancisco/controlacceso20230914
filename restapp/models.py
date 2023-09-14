from django.db import models

# Create your models here.

class PostCardIDEvent(models.Model):
    deviceID = models.CharField(max_length=8, null=True)
    cardID = models.CharField(max_length=8, null=False)
    f_evento = models.DateField(null=True)
    h_evento = models.TimeField(null=True)
    evento = models.CharField(max_length=50, null=True)
