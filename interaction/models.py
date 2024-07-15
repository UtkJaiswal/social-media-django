from django.db import models

from user.models import *

# Create your models here.
class Request(models.Model):
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,to_field='id',related_name='from_user')
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,to_field='id',related_name='to_user')
    status = models.CharField(max_length=10)

    