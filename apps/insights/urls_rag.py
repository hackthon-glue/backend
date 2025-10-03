"""
RAG Chat URL Configuration
"""

from django.urls import path
from .views.rag_chat_views import (
    RAGChatView,
    RAGSessionHistoryView,
    RAGSessionClearView,
    KnowledgeBaseQueryView
)

urlpatterns = [
    # Chat endpoints
    path('chat/', RAGChatView.as_view(), name='rag-chat'),
    path('chat/history/', RAGSessionHistoryView.as_view(), name='rag-history'),
    path('chat/session/', RAGSessionClearView.as_view(), name='rag-clear-session'),

    # Direct KB query (advanced)
    path('kb/query/', KnowledgeBaseQueryView.as_view(), name='kb-query'),
]
