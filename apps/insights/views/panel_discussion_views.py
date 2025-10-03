"""
Panel Discussion Views
API endpoints for viewing stored panel discussions
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services.panel_discussion_service import PanelDiscussionService


class PanelDiscussionListView(APIView):
    """List recent panel discussions"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = PanelDiscussionService()

    def get(self, request):
        """
        GET /api/insights/panel/discussions/

        Query params:
            - country_code (optional): Filter by country
            - limit (optional): Max results (default: 20)

        Returns:
            List of discussions with metadata
        """
        try:
            country_code = request.query_params.get('country_code')
            limit = int(request.query_params.get('limit', 20))

            discussions = self.service.list_discussions(
                country_code=country_code,
                limit=limit
            )

            return Response({
                'success': True,
                'data': {
                    'discussions': discussions,
                    'count': len(discussions),
                    'country_code': country_code
                }
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PanelDiscussionDetailView(APIView):
    """Get specific panel discussion"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = PanelDiscussionService()

    def get(self, request, discussion_id):
        """
        GET /api/insights/panel/discussions/<discussion_id>/

        Returns:
            Full discussion data including transcript
        """
        try:
            discussion = self.service.get_discussion(discussion_id)

            if not discussion:
                return Response({
                    'success': False,
                    'error': 'Discussion not found'
                }, status=status.HTTP_404_NOT_FOUND)

            return Response({
                'success': True,
                'data': discussion
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PanelDiscussionSummaryView(APIView):
    """Get discussion summary (lightweight)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = PanelDiscussionService()

    def get(self, request, discussion_id):
        """
        GET /api/insights/panel/discussions/<discussion_id>/summary/

        Returns:
            Summary without full transcript
        """
        try:
            summary = self.service.get_discussion_summary(discussion_id)

            if not summary:
                return Response({
                    'success': False,
                    'error': 'Discussion not found'
                }, status=status.HTTP_404_NOT_FOUND)

            return Response({
                'success': True,
                'data': summary
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CountryHistoryView(APIView):
    """Get discussion history for a country"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = PanelDiscussionService()

    def get(self, request, country_code):
        """
        GET /api/insights/panel/history/<country_code>/

        Query params:
            - limit (optional): Max results (default: 10)

        Returns:
            Discussion history with trend analysis
        """
        try:
            limit = int(request.query_params.get('limit', 10))

            history = self.service.get_country_history(
                country_code=country_code,
                limit=limit
            )

            return Response({
                'success': True,
                'data': history
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
