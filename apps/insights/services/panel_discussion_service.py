"""
Panel Discussion Service
Retrieves stored panel discussion results from S3
"""

import boto3
import json
from typing import Dict, List, Optional
from django.conf import settings
from django.core.cache import cache


class PanelDiscussionService:
    """Service for retrieving panel discussion results"""

    def __init__(self):
        self.s3_bucket = getattr(settings, 'PANEL_RESULTS_BUCKET', 'hackthon-panel-discussions')
        self.region = getattr(settings, 'AWS_REGION', 'ap-northeast-1')
        self.s3_client = boto3.client('s3', region_name=self.region)

    def list_discussions(
        self,
        country_code: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        """
        List recent panel discussions

        Args:
            country_code: Optional filter by country
            limit: Maximum number of results

        Returns:
            List of discussion metadata
        """
        cache_key = f"panel_discussions_{country_code or 'all'}_{limit}"
        cached = cache.get(cache_key)

        if cached:
            return cached

        try:
            prefix = f"discussions/{country_code}/" if country_code else "discussions/"

            response = self.s3_client.list_objects_v2(
                Bucket=self.s3_bucket,
                Prefix=prefix
            )

            discussions = []
            for obj in response.get('Contents', [])[:limit]:
                # Get metadata
                head = self.s3_client.head_object(
                    Bucket=self.s3_bucket,
                    Key=obj['Key']
                )

                metadata = head.get('Metadata', {})
                discussion_id = obj['Key'].split('/')[-1].replace('.json', '')

                discussions.append({
                    'discussion_id': discussion_id,
                    'country_code': metadata.get('country_code', 'UNKNOWN'),
                    'timestamp': obj['LastModified'].isoformat(),
                    'final_mood': metadata.get('final_mood', 'unknown'),
                    'final_score': float(metadata.get('final_score', 50)),
                    's3_key': obj['Key']
                })

            # Sort by timestamp descending
            discussions.sort(key=lambda x: x['timestamp'], reverse=True)

            # Cache for 5 minutes
            cache.set(cache_key, discussions, 300)

            return discussions

        except Exception as e:
            print(f"Error listing discussions: {e}")
            return []

    def get_discussion(self, discussion_id: str) -> Optional[Dict]:
        """
        Get full discussion by ID

        Args:
            discussion_id: Discussion ID

        Returns:
            Full discussion data or None
        """
        cache_key = f"panel_discussion_{discussion_id}"
        cached = cache.get(cache_key)

        if cached:
            return cached

        try:
            # Find the S3 key by listing
            discussions = self.list_discussions()
            s3_key = None

            for disc in discussions:
                if disc['discussion_id'] == discussion_id:
                    s3_key = disc['s3_key']
                    break

            if not s3_key:
                return None

            # Get full data from S3
            response = self.s3_client.get_object(
                Bucket=self.s3_bucket,
                Key=s3_key
            )

            data = json.loads(response['Body'].read())

            # Cache for 1 hour
            cache.set(cache_key, data, 3600)

            return data

        except Exception as e:
            print(f"Error getting discussion {discussion_id}: {e}")
            return None

    def get_country_history(
        self,
        country_code: str,
        limit: int = 10
    ) -> Dict:
        """
        Get discussion history for a country with trends

        Args:
            country_code: Country code
            limit: Maximum results

        Returns:
            Dict with discussions and trend analysis
        """
        discussions = self.list_discussions(country_code, limit)

        if not discussions:
            return {
                'country_code': country_code,
                'discussions': [],
                'trend': None
            }

        # Calculate trend
        trend = None
        if len(discussions) >= 2:
            latest = discussions[0]
            previous = discussions[1]

            trend = {
                'score_change': latest['final_score'] - previous['final_score'],
                'mood_change': self._compare_moods(
                    previous['final_mood'],
                    latest['final_mood']
                ),
                'direction': 'up' if latest['final_score'] > previous['final_score'] else 'down'
            }

        return {
            'country_code': country_code,
            'discussions': discussions,
            'trend': trend,
            'latest': discussions[0] if discussions else None
        }

    def get_discussion_summary(self, discussion_id: str) -> Optional[Dict]:
        """
        Get concise summary of a discussion

        Args:
            discussion_id: Discussion ID

        Returns:
            Summary dict or None
        """
        full_data = self.get_discussion(discussion_id)

        if not full_data:
            return None

        return {
            'discussion_id': discussion_id,
            'country_code': full_data['country_code'],
            'topic': full_data['topic'],
            'final_mood': full_data['final_mood'],
            'final_score': full_data['final_score'],
            'introduction': full_data['introduction'],
            'conclusion': full_data['conclusion'],
            'timestamp': full_data['metadata']['timestamp'],
            'total_turns': full_data['metadata']['total_turns'],
            'votes': full_data['votes']
        }

    def _compare_moods(self, old_mood: str, new_mood: str) -> str:
        """Compare two moods"""
        mood_order = {'sad': 0, 'neutral': 1, 'happy': 2}

        old_val = mood_order.get(old_mood, 1)
        new_val = mood_order.get(new_mood, 1)

        if new_val > old_val:
            return 'improving'
        elif new_val < old_val:
            return 'declining'
        else:
            return 'stable'
