from django.http import JsonResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer

from rest_framework.views import APIView
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
from .serializers import ResetPasswordRequestSerializer, SetNewPasswordSerializer
# from django.core.mail import send_mail

# test endpoint
def index(request):
    return JsonResponse({"message": "Accounts API is working!"})

User = get_user_model()

# Registration endpoint
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# Profile endpoint (view/update logged-in user)
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# Change password endpoint
# User = get_user_model()

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # check old password
            if not user.check_password(serializer.validated_data.get("old_password")):
                return Response({"old_password": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

            # set new password
            user.set_password(serializer.validated_data.get("new_password"))
            user.save()

            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Password reset request endpoint
class ResetPasswordRequestView(APIView):
    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "If that email exists, a reset link will be sent."})

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        # 🔥 For now, just return the link (in production, send via email)
        reset_link = f"http://localhost:8000/api/accounts/reset-password-confirm/?uidb64={uidb64}&token={token}"

        return Response({"reset_link": reset_link})

# class ResetPasswordRequestView(APIView):
#     def post(self, request):
#         email = request.data.get("email")
#         user = User.objects.filter(email=email).first()
#         if user:
#             uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#             token = default_token_generator.make_token(user)
#             reset_link = f"http://localhost:8000/api/accounts/reset-password-confirm/?uidb64={uidb64}&token={token}"

#             # Send reset link via email
#             send_mail(
#                 subject="Password Reset Request",
#                 message=f"Click the link below to reset your password:\n{reset_link}",
#                 from_email="noreply@metaltropic.com",
#                 recipient_list=[user.email],
#                 fail_silently=False,
#             )

#             return Response({"detail": "Password reset link sent to your email."}, status=200)

#         return Response({"detail": "User with this email does not exist."}, status=404)


class ResetPasswordConfirmView(APIView):
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        new_password = serializer.validated_data["new_password"]
        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password has been reset successfully."})