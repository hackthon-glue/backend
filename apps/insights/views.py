"""View logic for insights APIs."""
from __future__ import annotations

from rest_framework import viewsets

from .models import Country
from .serializers import CountrySerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset exposing countries with nested insights."""

    queryset = (
        Country.objects.all()
        .select_related("summary", "weather")
        .prefetch_related(
            "sentiments",
            "weather_trends",
            "news_items",
            "insight_stats",
            "alerts",
        )
    )
    serializer_class = CountrySerializer
    lookup_field = "code"
