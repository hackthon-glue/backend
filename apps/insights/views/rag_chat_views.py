"""
RAG Chat API Views
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
import uuid

from ..services.rag_chat_service import get_rag_service


class RAGChatView(APIView):
    """
    Chat with RAG Agent

    POST /api/insights/chat/
    {
        "message": "What's the current mood in Japan?",
        "session_id": "optional-session-id",
        "country_code": "JP"  // optional
    }
    """

    def post(self, request):
        message = request.data.get('message')

        if not message:
            return Response(
                {'error': 'Message is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create session ID
        session_id = request.data.get('session_id')
        if not session_id:
            session_id = str(uuid.uuid4())

        country_code = request.data.get('country_code')

        try:
            rag_service = get_rag_service()

            result = rag_service.chat(
                message=message,
                session_id=session_id,
                country_code=country_code
            )

            return Response({
                'success': True,
                'data': result
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RAGSessionHistoryView(APIView):
    """
    Get conversation history

    GET /api/insights/chat/history/?session_id=xxx
    """

    def get(self, request):
        session_id = request.query_params.get('session_id')

        if not session_id:
            return Response(
                {'error': 'session_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            rag_service = get_rag_service()
            history = rag_service.get_session_history(session_id)

            return Response({
                'success': True,
                'data': {
                    'session_id': session_id,
                    'history': history
                }
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RAGSessionClearView(APIView):
    """
    Clear conversation history

    DELETE /api/insights/chat/session/?session_id=xxx
    """

    def delete(self, request):
        session_id = request.query_params.get('session_id')

        if not session_id:
            return Response(
                {'error': 'session_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            rag_service = get_rag_service()
            rag_service.clear_session(session_id)

            return Response({
                'success': True,
                'message': 'Session cleared'
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class KnowledgeBaseQueryView(APIView):
    """
    Direct Knowledge Base query (advanced)

    POST /api/insights/kb/query/
    {
        "query": "Compare Japan and US mood trends",
        "country_code": "JP",  // optional filter
        "max_results": 5
    }
    """

    def post(self, request):
        query = request.data.get('query')

        if not query:
            return Response(
                {'error': 'Query is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        country_code = request.data.get('country_code')
        max_results = request.data.get('max_results', 5)

        try:
            rag_service = get_rag_service()

            result = rag_service.query_knowledge_base_directly(
                query=query,
                country_code=country_code,
                max_results=max_results
            )

            return Response({
                'success': True,
                'data': result
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
