from django.urls import path
from .views import SignupView, LoginView, FileUploadView, FileDownloadView, FileListView, EmailVerificationView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload-file/', FileUploadView.as_view(), name='file_upload'),
    path('download-file/<int:pk>/', FileDownloadView.as_view(), name='file_download'),
    path('file-list/', FileListView.as_view(), name='file_list'),
    path('verify-email/<str:token>/', EmailVerificationView.as_view(), name='email_verify'),  # Replace with your email verification view
]
