from rest_framework import permissions
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer,
    UpdateUserSerializer,
    UpdatePasswordSerializer,
    PasswordResetRequestSerializer,
    VerifyPasswordResetTokenSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework import status
from rest_framework.views import APIView
from .models import CustomUser as User

# Email sending
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from djangorestful.settings import FRONTEND_DOMAIN

# User = get_user_model()


class PasswordResetRequestView(APIView):

    serializer_class = PasswordResetRequestSerializer

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        # user = request.user

        if serializer.is_valid():
            serializer.save()

            user = User.objects.get(email=serializer.validated_data["email"])

            # current_site = get_current_site(self.request)

            subject = "Reset Password"
            message = render_to_string(
                "reset_password_email.html",
                {
                    "user": user,
                    "domain": FRONTEND_DOMAIN,
                    # 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    "token": user.get_reset_password_token(),
                },
            )
            user.email_user(subject, message)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(UpdateAPIView):

    permission_classes = [permissions.AllowAny]
    serializer_class = UpdatePasswordSerializer

    queryset = User.objects.all()

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = get_object_or_404(queryset, username=self.request.user)
    #     return obj

    def get_object(self):

        print(self)

        print("ss")
        queryset = self.get_queryset()
        #
        token = self.kwargs["token"]
        print(token)
        #
        obj = User.verify_reset_password_token(token)

        return obj


class VerifyPasswordResetTokenView(APIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()

    def post(self, request):
        serializer = VerifyPasswordResetTokenSerializer(data=request.data)
        # user = request.user

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # if request.user.is_authenticated

    # Get form data (current password, new pass 1 and 2,, validate it and set the new password


# @users.route('/password_reset/<token>', methods=['GET', 'POST'])
# def password_reset(token):
#
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
#
#     user = User.verify_reset_password_token(token)
#     if not user:
#         return redirect(url_for('index'))
#     form = PasswordResetForm()
#     if form.validate_on_submit():
#         user.set_password(form.password.data)
#         db.session.commit()
#         flash('Your password has been reset.')
#         return redirect(url_for('users.login'))
#     return render_template('reset_password.html', form=form)

# def request_password_reset():
#     form = RequestPasswordResetForm()

# if form.validate_on_submit():
#     print('validated on submit')
#     user = User.query.filter_by(email=form.email.data).first()
#     print("user {}".format(user))
#     if user:
#         token = user.get_reset_password_token()
#         msg = Message(
#             "Reset Password Instructions",
#             recipients=[user.email],
#             body=render_template(
#                 'email/reset_password.txt', user=user, token=token))
#         threaded_email_send(msg)
#         alert.info(
#             "Email with instructions have been sent to {}. Please check your e-mail."
#             .format(form.email.data))
#         return redirect(url_for('users.login'))
#     else:
#         alert.error('An user with that email does not exist')
#         return redirect(url_for('users.login'))
#
# return render_template("request_reset_password.html", form=form)


class LogoutView(APIView):
    def post(self, request):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class RegisterView(CreateAPIView):
    model = get_user_model()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class HelloWorldView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {"hello": "world"}
        return Response(content)


from rest_framework.generics import RetrieveAPIView
from .serializers import ModelSerializer
from django.shortcuts import get_object_or_404


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    # model = get_user_model()
    serializer_class = UserSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, username=self.request.user)
        return obj


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()

    # model = get_user_model()
    serializer_class = UpdateUserSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, username=self.request.user)
        return obj

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj = get_object_or_404(queryset, username=self.request.user)
    #     return obj
