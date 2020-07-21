# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta

from allauth.account.signals import password_changed
from django.conf import settings
from django.db import models
from django.utils import timezone


class PasswordExpiration(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    expiration_date = models.DateTimeField(null=False, blank=False, default=timezone.now)

    def expired(self):
        return self.expiration_date <= timezone.now()


def set_password_expiration(sender, user, **kwargs):
    pwd_exp, created = PasswordExpiration.objects.get_or_create(user=user)
    pwd_exp.expiration_date = datetime.now() + timedelta(days=getattr(settings, 'PASSWORD_VALIDATION_DAYS', 90))
    pwd_exp.save()


password_changed.connect(set_password_expiration)
