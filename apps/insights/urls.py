"""URL routes for insights APIs."""
from __future__ import annotations

from rest_framework.routers import DefaultRouter

from .views import CountryViewSet, PanelDiscussionViewSet

router = DefaultRouter()
router.register("countries", CountryViewSet, basename="country")
router.register("panels", PanelDiscussionViewSet, basename="panel")

urlpatterns = router.urls
