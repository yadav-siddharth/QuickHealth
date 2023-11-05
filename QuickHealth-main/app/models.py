from django.db import models

# Create your models here.
class Patient(models.Model):
    Firstname=models.CharField(max_length=70)
    Lastname=models.CharField(max_length=70)
    Email=models.CharField(max_length=70)
    Contact=models.BigIntegerField()
    Username=models.CharField(max_length=10,unique=True)
    Password=models.CharField(max_length=10)
    Date=models.CharField(max_length=500,default="")
    Time=models.CharField(max_length=500,default="")
    Link=models.CharField(max_length=1000,default="")
    Wallet=models.BigIntegerField(default=0)
    Doctors=models.CharField(max_length=500,default="")
                   
    def __str__(self) -> str:
        return self.Firstname
    
class Doctor(models.Model):
    Firstname=models.CharField(max_length=70)
    Lastname=models.CharField(max_length=70)
    Email=models.CharField(max_length=70)
    Contact=models.BigIntegerField()
    Username=models.CharField(max_length=10,unique=True)
    Password=models.CharField(max_length=10)
    Speciality=models.CharField(max_length=50,default="")
    Experience=models.IntegerField(default="")
    Slots=models.CharField(max_length=200,default="")
    C_fees=models.IntegerField(default="")
    Wallet=models.BigIntegerField(default=0)
    
    def __str__(self) -> str:
        return self.Firstname
    
class Appointment(models.Model):
    DoctorId=models.CharField(max_length=50)
    PatientId=models.CharField(max_length=500)
    Dates=models.CharField(max_length=500)
    Slots=models.CharField(max_length=500)
    
    def __str__(self) -> str:
        return self.DoctorId