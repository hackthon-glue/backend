"""Panel discussion URL routes"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PanelDiscussionViewSet

router = DefaultRouter()
router.register(r'panels', PanelDiscussionViewSet, basename='panel')

urlpatterns = [
    path('', include(router.urls)),
]
