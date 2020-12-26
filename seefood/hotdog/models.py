from django.db import models


# Create your models here.
class Image(models.Model):
    file = models.ImageField(upload_to='images/')
    time= models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)