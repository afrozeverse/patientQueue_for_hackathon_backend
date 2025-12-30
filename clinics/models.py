from django.db import models
from users.models import User
import uuid

class ClinicProfile(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    clinic_name=models.CharField(max_length=100)
    specialization=models.CharField(max_length=50)
    # short code for booking - user can think as a username selection
    public_code=models.CharField(max_length=50)

    def __str__(self):
        return str(self.public_code)
    
class Session(models.Model):
    SESSION_CHOICES=(
        ('MORNING','Morning'),
        ('EVENING','Evening')
    )
    BOOKING_STATUS_CHOICES=(
        ('OPEN','Open'),
        ('CLOSE','Close')
    )
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    clinic=models.ForeignKey(ClinicProfile, on_delete=models.CASCADE)
    session_name=models.CharField(max_length=10,choices=SESSION_CHOICES,default='MORNING')
    visiting_charge=models.CharField(max_length=12)
    avg_consultation_time=models.CharField(max_length=10) #in minutes
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    booking_status=models.CharField(max_length=10,choices=BOOKING_STATUS_CHOICES,default='OPEN')
    last_token_number=models.IntegerField(default=0)
    total_tokens=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)        


    