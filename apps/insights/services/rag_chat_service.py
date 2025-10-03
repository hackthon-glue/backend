"""
RAG Chat Service - Bedrock Agent with Knowledge Base integration
"""

import boto3
import os
from typing import List, Dict, Optional
from django.core.cache import cache


class RAGChatService:
    """Service for interacting with RAG Chat Agent"""

    def __init__(self):
        self.bedrock_runtime = boto3.client(
            'bedrock-agent-runtime',
            region_name=os.getenv('AWS_REGION', 'ap-northeast-1')
        )

        # Agent IDs from environment
        self.rag_agent_id = os.getenv('RAG_AGENT_ID')
        self.rag_agent_alias_id = os.getenv('RAG_AGENT_ALIAS_ID', 'TSTALIASID')
        self.knowledge_base_id = os.getenv('KNOWLEDGE_BASE_ID')

        if not self.rag_agent_id:
            raise ValueError("RAG_AGENT_ID environment variable not set")

    def chat(
        self,
        message: str,
        session_id: str,
        country_code: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Send a chat message to RAG agent

        Args:
            message: User message
            session_id: Session ID for conversation continuity
            country_code: Optional country code for context filtering

        Returns:
            Dict with response and metadata
        """

        # Add country context if provided
        if country_code:
            contextualized_message = f"[Context: User is asking about {country_code}]\n\n{message}"
        else:
            contextualized_message = message

        try:
            # Invoke agent with streaming
            response = self.bedrock_runtime.invoke_agent(
                agentId=self.rag_agent_id,
                agentAliasId=self.rag_agent_alias_id,
                sessionId=session_id,
                inputText=contextualized_message,
                enableTrace=True  # Enable for debugging
            )

            # Extract response from stream
            full_response = ""
            citations = []
            trace_data = []

            for event in response.get('completion', []):
                if 'chunk' in event:
                    chunk = event['chunk']
                    if 'bytes' in chunk:
                        full_response += chunk['bytes'].decode('utf-8')

                    # Extract citations if available
                    if 'attribution' in chunk:
                        attribution = chunk['attribution']
                        if 'citations' in attribution:
                            citations.extend(attribution['citations'])

                # Capture trace for debugging
                if 'trace' in event:
                    trace_data.append(event['trace'])

            # Store session in cache (30 min TTL)
            cache_key = f"rag_session_{session_id}"
            session_history = cache.get(cache_key, [])
            session_history.append({
                'role': 'user',
                'content': message
            })
            session_history.append({
                'role': 'assistant',
                'content': full_response
            })
            cache.set(cache_key, session_history, timeout=1800)

            return {
                'response': full_response.strip(),
                'session_id': session_id,
                'citations': self._format_citations(citations),
                'has_kb_results': len(citations) > 0
            }

        except Exception as e:
            raise Exception(f"RAG chat failed: {str(e)}")

    def _format_citations(self, citations: List[Dict]) -> List[Dict]:
        """Format citations for frontend display"""
        formatted = []

        for citation in citations:
            retrieved_references = citation.get('retrievedReferences', [])

            for ref in retrieved_references:
                formatted.append({
                    'content': ref.get('content', {}).get('text', ''),
                    'location': ref.get('location', {}).get('s3Location', {}),
                    'metadata': ref.get('metadata', {})
                })

        return formatted

    def get_session_history(self, session_id: str) -> List[Dict]:
        """Get conversation history for a session"""
        cache_key = f"rag_session_{session_id}"
        return cache.get(cache_key, [])

    def clear_session(self, session_id: str):
        """Clear conversation history"""
        cache_key = f"rag_session_{session_id}"
        cache.delete(cache_key)

    def query_knowledge_base_directly(
        self,
        query: str,
        country_code: Optional[str] = None,
        max_results: int = 5
    ) -> Dict:
        """
        Direct Knowledge Base query (without agent)
        Useful for advanced searches
        """
        if not self.knowledge_base_id:
            raise ValueError("KNOWLEDGE_BASE_ID not configured")

        kb_client = boto3.client('bedrock-agent-runtime')

        # Build retrieval configuration
        retrieval_config = {
            'vectorSearchConfiguration': {
                'numberOfResults': max_results
            }
        }

        # Add country filter if specified
        if country_code:
            retrieval_config['vectorSearchConfiguration']['filter'] = {
                'equals': {
                    'key': 'country',
                    'value': country_code
                }
            }

        try:
            response = kb_client.retrieve_and_generate(
                input={'text': query},
                retrieveAndGenerateConfiguration={
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'knowledgeBaseId': self.knowledge_base_id,
                        'modelArn': f'arn:aws:bedrock:{os.getenv("AWS_REGION", "ap-northeast-1")}::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0',
                        'retrievalConfiguration': retrieval_config
                    }
                }
            )

            return {
                'response': response['output']['text'],
                'citations': response.get('citations', [])
            }

        except Exception as e:
            raise Exception(f"Knowledge Base query failed: {str(e)}")


# Singleton instance
_rag_service = None


def get_rag_service() -> RAGChatService:
    """Get or create RAG service instance"""
    global _rag_service

    if _rag_service is None:
        _rag_service = RAGChatService()

    return _rag_service