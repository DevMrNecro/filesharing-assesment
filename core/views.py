from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import File, CustomUser
from .serializers import UserSerializer, FileSerializer
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.conf import settings


class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        verification_url = f"{self.request.build_absolute_uri('/api/verify-email/')}{token.key}/"


        send_mail(
            subject='Verify your email',
            message=f'Please verify your email by clicking on the link: {verification_url}',
            from_email='eazeallianceservices@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({"token": token.key, "message": "User created. Verification email sent."}, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer  

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user_id": user.id, "username": user.username, "message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class EmailVerificationView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token, *args, **kwargs):
        try:
            user_token = Token.objects.get(key=token)
            user = user_token.user
            user.is_active = True
            user.save()

            return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
        
        except Token.DoesNotExist:
            return Response({"message": "Invalid token!"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FileUploadView(generics.CreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != 'ops':
            return Response({"message": "Only Operations Users can upload files."}, status=status.HTTP_403_FORBIDDEN)
        serializer.save(uploader=user)

class FileDownloadView(generics.RetrieveAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        file_instance = self.get_object()
        if request.user.user_type != 'client':
            return Response({"message": "Access denied"}, status=status.HTTP_403_FORBIDDEN)
        
        secure_link = f"{request.build_absolute_uri('/api/download-file/')}{file_instance.id}/?token={Token.objects.get(user=request.user).key}"
        return Response({"download-link": secure_link, "message": "success"})

class FileListView(generics.ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(uploader=self.request.user)
