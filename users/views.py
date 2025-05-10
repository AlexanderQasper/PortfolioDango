import logging
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView

from axes.handlers.proxy import AxesProxyHandler
from axes.helpers import get_client_username
from .serializers import UserRegistrationSerializer, UserProfileSerializer, UserSerializer
from .permissions import IsSelfOrAdmin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User

logger = logging.getLogger(__name__)
User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Use email as the primary login field
        email = request.data.get("email", "").strip()
        user = User.objects.filter(email=email).first()
        
        # Check if the email has been verified before allowing login
        if user and not user.is_email_verified:
            raise AuthenticationFailed("Please verify your email before logging in.")

        if AxesProxyHandler().is_locked(request):
            logger.warning(f"🔒 User '{email}' is locked out.")
            raise AuthenticationFailed("Account is locked due to too many login attempts.")

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            AxesProxyHandler().reset_attempts()
            logger.info(f"✅ Successful login for user '{email}'. Lockout counter reset.")
        else:
            AxesProxyHandler().user_login_failed(
                sender=self.__class__,
                request=request,
                credentials={"email": email}
            )
            logger.warning(f"❌ Failed login attempt for user '{email}'.")

        return response


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.send_verification_email()


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsSelfOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def verify_email(self, request):
        token = request.data.get('token')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email_verification_token=token)
            if user.is_email_verified:
                return Response({'error': 'Email already verified'}, status=status.HTTP_400_BAD_REQUEST)

            user.is_email_verified = True
            user.save()
            return Response({'status': 'Email verified successfully'})
        except User.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def resend_verification(self, request):
        user = request.user
        if user.is_email_verified:
            return Response({'error': 'Email already verified'}, status=status.HTTP_400_BAD_REQUEST)

        if user.email_verification_sent_at:
            time_since_last = timezone.now() - user.email_verification_sent_at
            if time_since_last.total_seconds() < 300:
                return Response({'error': 'Please wait before requesting another verification email'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        user.send_verification_email()
        return Response({'status': 'Verification email sent'})