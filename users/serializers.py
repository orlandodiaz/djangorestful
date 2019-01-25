from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    ValidationError,
    CharField,
    IntegerField,
    EmailField,
    BooleanField,
)

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import CustomUser as User
from .models import Profile

import django.contrib.auth.password_validation as validators

# User = get_user_model()
from django.contrib.auth import authenticate

# Email sending
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode


class PasswordResetRequestSerializer(Serializer):

    email = EmailField()

    def validate_email(self, email):

        print("email from validate:", email)
        try:
            User.objects.get(email=email)
            return email
        except User.DoesNotExist:
            raise ValidationError("That email is not associated with any user")

    def save(self):
        """


        Returns:

        """
        print("self.validated_data['email']", self.validated_data["email"])
        pass


class UserSerializer(ModelSerializer):
    email_confirmed = BooleanField(source="profile.email_confirmed", read_only=True)

    class Meta:
        model = User
        # write_only_fields = ("password",)


        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "email_confirmed",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user


class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        # write_only_fields = ("password",)
        fields = ("username", "email", "first_name", "last_name")
        # extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            # if attr == "password":
            #     setattr(instance, attr, value)
            #     instance.set_password(validated_data["password"])
            #     instance.save()
            # else:
            setattr(instance, attr, value)
            instance.save()
        return instance


class VerifyPasswordResetTokenSerializer(Serializer):
    token = CharField()

    class Meta:
        fields = ("token",)

    def validate_token(self, token):
        print(token)
        user = User.verify_reset_password_token(token)
        print(User.verify_reset_password_token(token))
        if not user:
            raise ValidationError("Token is invalid")

    def save(self):
        token = self.validated_data["token"]


class UpdatePasswordSerializer(ModelSerializer):
    new_password = CharField(write_only=True)
    new_password1 = CharField(write_only=True)

    # token = CharField()

    class Meta:
        model = User
        fields = ("new_password", "new_password1")
        extra_kwargs = {
            "new_password": {"write_only": True},
            "new_password1": {"write_only": True},
        }

    def validate(self, data):
        """  Method to validate data on multiple fields at once
        Args:
            self (UpdatePasswordSerializer): Contains the request object,
                data object (all data received).
            data (OrderedDict): Data received by user that EXISTS in the model.
                                If you want all data  use self.initial_data instead
                                or even better specify them above
                                Raise ValidationError exception here

        Returns:
            data (OrderedDict): Return the data object if validation passed

        """
        kwargs = self.context["view"].kwargs

        token = kwargs["token"]

        print(token)
        user = User.verify_reset_password_token(token)
        print(User.verify_reset_password_token(token))
        if not user:
            raise ValidationError("Token is invalid")

        if not data.get("new_password"):
            raise ValidationError("new_password is required")

        if not data.get("new_password1"):
            raise ValidationError("new_password1 is required")

        print("request object:", self.context["request"])

        if not token:
            raise ValidationError("Token is needed")

        if data["new_password"] != data["new_password1"]:
            raise ValidationError("Passwords don't match")

        return data

    # def validate_token(self, token):
    #     print(token)
    #     user = User.verify_reset_password_token(token)
    #     print(User.verify_reset_password_token(token))
    #     if not user:
    #         raise ValidationError("Token is invalid")
    #

    # def validate_password(self, password):
    #     """  Validate on an specific received field value that EXISTS in the model
    #     Args:
    #         field (str): The value received that is specified in fields above
    #                      Raise ValidationError here
    #
    #     Returns:
    #         field (str): Validated field
    #
    #     """
    #     # print("current_password:", password)
    #     # print("self.context['request'].user", self.context["request"].user)
    #
    #     user = self.context["request"].user
    #
    #     if not authenticate(username=user, password=password):
    #         raise ValidationError("Current password is incorrect")
    #
    #     return password

    def update(self, instance, validated_data):
        """  Update model instance
        Args:
            instance (obj): The instance of the current user
            validated_data (dict): Dictionary of validated data

        Returns:
            instance (obj): The user instance

        """
        # print(instance, "instance")
        # print("instance type:", type(instance))
        print("validated_data:", validated_data)
        # print("validated_data type:", type(validated_data))
        for attr, value in validated_data.items():
            if attr == "new_password":
                setattr(instance, attr, value)
                instance.set_password(validated_data["new_password"])
                instance.save()
        return instance
