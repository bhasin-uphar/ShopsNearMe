from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'shop'