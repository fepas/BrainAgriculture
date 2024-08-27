from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RuralProducerViewSet, general_statistics

router = DefaultRouter()
router.register(r"producers", RuralProducerViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("general_statistics/", general_statistics, name="general_statistics"),
]
