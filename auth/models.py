from django.db import models

# Create your models here.

#Support Engineer details
class Engineer(models.Model):
    email = models.EmailField(max_length=128, unique=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    
    #Gives quick information about the engineer object
    def __str__(self):
        return "Engineer is "self.first_name+" "+self.last_name




#Devices found in the lab
class Device(models.Model):
    serialnumber = models.CharField(max_length=12,unique=True)
    device_model = models.CharField(max_length=12)
    device_type = models.CharField(max_length=24)
    x0_ip = models.GenericIPAddressField(max_length=15)
    x0_subnetmask = models.GenericIPAddressField(max_length=15)
    x1_ip = models.GenericIPAddressField(max_length=15)
    x1_subnetmask = models.GenericIPAddressField(max_length=15)
    x1_gateway = models.GenericIPAddressField(max_length=15)
    x3_ip = models.GenericIPAddressField(max_length=15)
    x3_subnetmask = models.GenericIPAddressField(max_length=15)
    x3_gateway = models.GenericIPAddressField(max_length=15)
    podnumber = models.IntegerField()
    firmware = models.CharField()

    #Gives quick information about the device object
    def __str__(self):
        return "Device: "+self.device_type+", Model: "+self.device_model+", Serialnumber: "+self.serialnumber




#Tracks the request history of a device
class RequestHistory(models.Model):
    email = models.ForeignKey('Engineer', on_delete=models.SET_NULL)
    serialnumber = models.ForeignKey('Device', on_delete=models.SET_NULL)
    date_requested = models.DateField()
    time_requested = models.TimeField()
    date_returned = models.DateField()
    time_returned = models.TimeField()
    available = models.BooleanField()

    def __str__(self):
        return "Engineer's email: "+self.email+", Serialnumber of device: "+self.serialnumber

