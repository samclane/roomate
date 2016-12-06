from __future__ import unicode_literals

import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# class Roomate(models.Model):
#     user = models.OneToOneField(User)
#     rid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     rname_first = models.CharField(max_length=128)
#     rname_last = models.CharField(max_length=128)
#     def __str__(self):
#         return self.rname_first + " " + self.rname_last

class Bill(models.Model):
    bname = models.CharField(max_length=128)
    company = models.CharField(max_length=512)
    if_purchased = models.BooleanField(default=False)
    due_date = models.DateField()
    total_cost = models.DecimalField(max_digits=65, decimal_places=2)
    remaining_cost = models.DecimalField(max_digits=65, decimal_places=2, default=0.0)
    creation_date = models.DateField(auto_created=True, editable=False, auto_now=True)


class Grocery(models.Model):
    gname = models.CharField(max_length=128)
    store = models.CharField(max_length=128)
    if_purchased = models.BooleanField(default=False)
    purchaser = models.ForeignKey(User, on_delete=models.CASCADE)
    total_cost = models.DecimalField(max_digits=65, decimal_places=2)
    remaining_cost = models.DecimalField(max_digits=65, decimal_places=2, default=0.0)
    creation_date = models.DateField(auto_created=True, editable=False,auto_now=True)


class Chore(models.Model):
    name = models.CharField(max_length=128)
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    if_complete = models.BooleanField(default=False)
    creation_date = models.DateField(auto_created=True, editable=False, auto_now=True)

    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         profile, created = Roomate.objects.get_or_create(user=instance)
    #
    # post_save.connect(create_user_profile, sender=User)
