"""
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Support Engineer details
class Engineer(models.Model):
    #Create relationship (don't inherit from User)
    engineer = models.OneToOneField(User)
    
    #Gives quick information about the engineer object
    def __str__(self):
        return "Engineer: "+self.engineer.first_name+" "+self.engineer.last_name    

"""

