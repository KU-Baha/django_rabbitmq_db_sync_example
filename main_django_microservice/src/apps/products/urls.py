from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, UserAPIView

router = DefaultRouter()

router.register(r"products", ProductViewSet, "product")

urlpatterns = [
    path("user/", UserAPIView.as_view()),
]

urlpatterns += router.urls
