"""Serializers for insights app."""
from __future__ import annotations

from rest_framework import serializers

from .models import (
    Country,
    CountryNewsItem,
    CountrySentiment,
    CountrySummary,
    CountryWeather,
    PanelDiscussion,
    PanelExpertAnalysis,
    PanelVote,
    PanelTranscript,
)


class CountrySentimentSerializer(serializers.ModelSerializer):
    """Serialize sentiment points for the chart."""

    date = serializers.SerializerMethodField()

    class Meta:
        model = CountrySentiment
        fields = ["date", "score"]

    def get_date(self, obj: CountrySentiment) -> str:
        """Return a label or ISO date for the point."""
        if obj.label:
            return obj.label
        if obj.recorded_date:
            return obj.recorded_date.isoformat()
        return ""


class CountryNewsItemSerializer(serializers.ModelSerializer):
    """Serialize curated news feeds."""

    class Meta:
        model = CountryNewsItem
        fields = ["title", "summary", "url", "category", "tone"]


class CountryWeatherSerializer(serializers.ModelSerializer):
    """Serialize current weather details."""

    feelsLike = serializers.IntegerField(source="feels_like")
    precipitationChance = serializers.IntegerField(source="precipitation_chance")

    class Meta:
        model = CountryWeather
        fields = [
            "condition",
            "temperature",
            "feelsLike",
            "humidity",
            "wind",
            "precipitationChance",
        ]


class CountryInsightsSerializer(serializers.Serializer):
    """Nested representation of insight payload expected by the frontend."""

    sentiment = CountrySentimentSerializer(many=True, source="sentiments")
    news = CountryNewsItemSerializer(many=True, source="news_items")
    weatherNow = CountryWeatherSerializer(source="weather")
    moodNarrative = serializers.CharField(source="summary.mood_narrative")
    todaySummary = serializers.CharField(source="summary.today_summary")


class CountrySummarySerializer(serializers.ModelSerializer):
    """Serialize the summary block for a country."""

    class Meta:
        model = CountrySummary
        fields = ["headline", "weather", "persona"]


class CountrySerializer(serializers.ModelSerializer):
    """Serialize a country and its insights in the structure used by the UI."""

    lat = serializers.FloatField(source="latitude")
    lng = serializers.FloatField(source="longitude")
    summary = CountrySummarySerializer(read_only=True)
    insights = CountryInsightsSerializer(source="*")

    class Meta:
        model = Country
        fields = ["code", "name", "lat", "lng", "summary", "insights"]


# ============================================================================
# Panel Discussion Serializers
# ============================================================================

class PanelTranscriptSerializer(serializers.ModelSerializer):
    """Serialize panel transcript"""

    class Meta:
        model = PanelTranscript
        fields = ["speaker", "content", "round_number", "turn_order"]


class PanelVoteSerializer(serializers.ModelSerializer):
    """Serialize panel vote"""

    class Meta:
        model = PanelVote
        fields = ["expert_role", "vote_mood", "confidence", "reasoning"]


class PanelExpertAnalysisSerializer(serializers.ModelSerializer):
    """Serialize expert analysis"""

    class Meta:
        model = PanelExpertAnalysis
        fields = ["expert_role", "analysis_text", "round_number"]


class PanelDiscussionSerializer(serializers.ModelSerializer):
    """Serialize complete panel discussion"""

    analyses = PanelExpertAnalysisSerializer(many=True, read_only=True)
    votes = PanelVoteSerializer(many=True, read_only=True)
    transcripts = PanelTranscriptSerializer(many=True, read_only=True)

    class Meta:
        model = PanelDiscussion
        fields = [
            "id",
            "country_code",
            "topic",
            "final_mood",
            "final_score",
            "introduction",
            "conclusion",
            "discussion_date",
            "total_turns",
            "debate_rounds",
            "created_at",
            "analyses",
            "votes",
            "transcripts",
        ]


class PanelDiscussionListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing discussions"""

    class Meta:
        model = PanelDiscussion
        fields = [
            "id",
            "country_code",
            "topic",
            "final_mood",
            "final_score",
            "discussion_date",
            "created_at",
        ]
