from django.db import models
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from django.db.models.signals import post_save, pre_save
from kroon.users.models import User

# Create your models here.


