from django.urls import path, include
from faces import views
from django.conf.urls.static import static

urlpatterns = [
    path('face_enrollment/', views.FaceEnrollmentView.as_view(), name='faceenrollment'),
    path('face_detect/', views.FaceDetectView.as_view(), name='facedetect'),
]