from django.db import models

# Create your models here.

class Engineer(models.Model):
    email = models.EmailField(max_length=128, unique=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    
def __str__(self):
        return self.first_name+" "+self.last_name




class device(models.Model):
    

    
