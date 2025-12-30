from django.db import models
from clinics.models import Session
from users.models import User
import uuid

class Token(models.Model):
    STATUS_CHOICES=(
        ('WAITING','Waiting'),
        ('DONE','Done'),
        ('SKIPPED','Skipped'),
    )
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    session=models.ForeignKey(Session,on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    token_number=models.IntegerField()
    status=models.CharField(max_length=15,choices=STATUS_CHOICES,default='WAITING')
    created_at = models.DateTimeField(auto_now_add=True)

    #Prevents same user getting multiple tokens for the same session
    class Meta:
        unique_together = (
            ('user', 'session'),
            ('session', 'token_number'),
        )
