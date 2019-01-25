from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
import jwt
from time import time
from django.conf.global_settings import SECRET_KEY


class CustomUser(AbstractUser):
    email = CharField(max_length=200, unique=True)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.pk, "exp": time() + expires_in},
            SECRET_KEY,
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])[
                "reset_password"
            ]
        except:
            return
        return CustomUser.objects.get(pk=id)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
