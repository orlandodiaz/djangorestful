from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
import jwt
from time import time
from django.conf.global_settings import SECRET_KEY
from backend.settings.base import FRONTEND_DOMAIN



from django.template.loader import (render_to_string)

class CustomUser(AbstractUser):
    email = CharField(max_length=200, unique=True)

    def get_verify_email_token(self, expires_in=600):
        return jwt.encode(
            {"verify_email": self.pk, "exp": time() + expires_in},
            SECRET_KEY,
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_email_token(token):
        try:
            id = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])[
                "verify_email"
            ]
        except:
            return
        return CustomUser.objects.get(pk=id)

    def send_verification_email(self):
        token = self.get_verify_email_token()

        subject = "Confirm your email"
        message = render_to_string(
            "verify_email.html",
            {
                "user": self,
                "domain": FRONTEND_DOMAIN,
                # 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                "token": token,
            },
        )
        self.email_user(subject, message)

    # def send_verification_email(self):
    #     token = self.get_verify_email_token()
    #
    #     msg = Message(
    #         "Verify your email",
    #         recipients=[self.email],
    #         body=render_template(
    #             'email/email_verification.txt', user=self, token=token))
    #     threaded_email_send(msg)
    #
    # def get_verify_email_token(self, expires_in=600):
    #     return jwt.encode({
    #         'verify_email_token': self.id,
    #         'exp': time() + expires_in
    #     },
    #                       app.config['SECRET_KEY'],
    #                       algorithm='HS256').decode('utf-8')
    #
    # @staticmethod
    # def verify_email_token(token):
    #     try:
    #         id = jwt.decode(
    #             token, app.config['SECRET_KEY'],
    #             algorithms=['HS256'])['verify_email_token']
    #     except:
    #         return
    #     return User.query.get(id)

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
