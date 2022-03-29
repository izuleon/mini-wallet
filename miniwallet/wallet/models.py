from datetime import datetime, timezone
from django.db import models
import uuid

from customer.models import Customer
ENABLE_CHOICES = (
    ('enabled', 'enabled'),
    ('disabled', 'disabled')
)
SUCCESS_CHOICES = (
    ('success', 'success'),
    ('unsuccesful', 'unsuccesful')
)
# Create your models here.
class Wallet(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    balance = models.PositiveBigIntegerField(default=0)
    owned_by = models.ForeignKey(Customer, models.CASCADE)
    status = models.CharField(max_length=10, default="enabled", choices=ENABLE_CHOICES)
    now_object = datetime.now(tz=timezone.utc)
    now = now_object.isoformat()
    enabled_at = models.DateTimeField(default=now)


class Deposits(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    deposited_by = models.ForeignKey(Customer, models.CASCADE)
    owned_by = models.ForeignKey(Wallet, models.CASCADE)
    status = models.CharField(max_length=15, default="enabled", choices=SUCCESS_CHOICES)
    deposited_at = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveBigIntegerField(default=0)
    reference_id = models.UUIDField(default=uuid.uuid4, unique=True)


class Withdrawals(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    withdrawn_by = models.ForeignKey(Customer, models.CASCADE)
    owned_by = models.ForeignKey(Wallet, models.CASCADE)
    status = models.CharField(max_length=15, default="enabled", choices=SUCCESS_CHOICES)
    withdrawn_at = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveBigIntegerField(default=0)
    reference_id = models.UUIDField(default=uuid.uuid4, unique=True)
