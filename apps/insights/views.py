"""View logic for insights APIs."""
from __future__ import annotations

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Country, PanelDiscussion
from .serializers import CountrySerializer, PanelDiscussionSerializer, PanelDiscussionListSerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset exposing countries with nested insights."""

    queryset = (
        Country.objects.all()
        .select_related("summary", "weather")
        .prefetch_related(
            "sentiments",
            "news_items",
        )
    )
    serializer_class = CountrySerializer
    lookup_field = "code"


class PanelDiscussionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Panel discussion results API

    list: Get all panel discussions
    retrieve: Get specific panel discussion with full details
    latest_by_country: Get latest discussion for a country
    """

    queryset = PanelDiscussion.objects.prefetch_related(
        'analyses', 'votes', 'transcripts'
    ).all()

    def get_serializer_class(self):
        """Use lightweight serializer for list view"""
        if self.action == 'list':
            return PanelDiscussionListSerializer
        return PanelDiscussionSerializer

    @action(detail=False, methods=['get'], url_path='country/(?P<country_code>[^/.]+)')
    def latest_by_country(self, request, country_code=None):
        """
        Get latest panel discussion for a specific country

        GET /api/panels/country/{country_code}/
        """
        discussion = PanelDiscussion.objects.filter(
            country_code=country_code
        ).prefetch_related(
            'analyses', 'votes', 'transcripts'
        ).order_by('-discussion_date', '-id').first()

        if not discussion:
            return Response(
                {'error': f'No discussion found for country {country_code}'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = PanelDiscussionSerializer(discussion)
        return Response(serializer.data)
