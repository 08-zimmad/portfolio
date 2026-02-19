from django.urls import include, path
from rest_framework.routers import DefaultRouter

from my_portal import views

router = DefaultRouter()
router.register(r"education", views.EducationAPIView, basename="education")

urlpatterns = [
    path("login", views.LoginApiView.as_view(), name="login"),
    path("register", views.RegisterApiView.as_view(), name="register"),
    path("api/", include(router.urls)),
]
