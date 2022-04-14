from datetime import timedelta
import uuid
import random
import string
from .sender import send_otp
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser



class OtpRequestQueryset(models.QuerySet):

    def is_valid(self, receiver, request, password):
        current_time = timezone.now()
        return self.filter(
            receiver=receiver,
            request_id=request,
            password=password,
            created__lt=current_time,
            created__gt=current_time-timedelta(seconds=120),

        ).exists()


class OtpManager(models.Manager):

    def get_queryset(self):
        return OtpRequestQueryset(self.model, self._db)
    def is_valid(self, receiver, request, password):
        return self.get_queryset().is_valid(receiver, request, password)

    def generate(self, data):
        otp = self.model(channel=data['channel'], receiver=data['receiver'])
        otp.save(using=self._db)
        send_otp(otp)
        return otp

def otp_generate():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits, k = 4)
    return ''.join(digits)


class CostumeUser(AbstractUser):
    pass


class OtpRequest(models.Model):
    class OtpChannel(models.TextChoices): 
        PHONE = 'Phone'
        EMAIL = 'E_Mail'
    request_id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    channel = models.CharField(max_length=12, blank=True, 
        choices =OtpChannel.choices, default = OtpChannel.PHONE )
    receiver = models.CharField(max_length=10)
    password = models.CharField(max_length=6, default = otp_generate)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    objects = OtpManager()