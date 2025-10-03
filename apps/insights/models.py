"""Database models representing country insights."""
from __future__ import annotations

from django.db import models


class Country(models.Model):
    """Reference data for a country."""

    code = models.CharField(max_length=8, unique=True)
    name = models.CharField(max_length=128)
    latitude = models.DecimalField(max_digits=8, decimal_places=5)
    longitude = models.DecimalField(max_digits=8, decimal_places=5)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.code.upper()})"


class CountrySummary(models.Model):
    """High-level summary block displayed on the dashboard."""

    country = models.OneToOneField(
        Country,
        on_delete=models.CASCADE,
        related_name="summary",
    )
    headline = models.CharField(max_length=255)
    weather = models.CharField(max_length=255)
    persona = models.CharField(max_length=255)
    mood_narrative = models.TextField()
    today_summary = models.TextField()

    class Meta:
        verbose_name = "Country summary"
        verbose_name_plural = "Country summaries"

    def __str__(self) -> str:
        return f"Summary for {self.country.code.upper()}"


class CountryWeather(models.Model):
    """Current weather snapshot for a country."""

    country = models.OneToOneField(
        Country,
        on_delete=models.CASCADE,
        related_name="weather",
    )
    condition = models.CharField(max_length=128)
    temperature = models.SmallIntegerField()
    feels_like = models.SmallIntegerField()
    humidity = models.PositiveSmallIntegerField()
    wind = models.CharField(max_length=64)
    precipitation_chance = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Country weather"
        verbose_name_plural = "Country weather"

    def __str__(self) -> str:
        return f"Weather for {self.country.code.upper()}"


class CountrySentiment(models.Model):
    """Sentiment score at a point in time."""

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="sentiments",
    )
    label = models.CharField(max_length=32)
    recorded_date = models.DateField(blank=True, null=True)
    score = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["recorded_date", "id"]

    def __str__(self) -> str:
        if self.label:
            return f"{self.country.code.upper()} sentiment {self.label}"
        return f"Sentiment point {self.pk}"


class CountryNewsItem(models.Model):
    """Curated news entries influencing sentiment."""

    class Tone(models.TextChoices):
        CELEBRATORY = "celebratory", "Celebratory"
        OPTIMISTIC = "optimistic", "Optimistic"
        CAUTIOUS = "cautious", "Cautious"
        URGENT = "urgent", "Urgent"

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="news_items",
    )
    title = models.CharField(max_length=255)
    summary = models.TextField()
    url = models.URLField(max_length=500)
    category = models.CharField(max_length=64)
    tone = models.CharField(max_length=16, choices=Tone.choices)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.country.code.upper()} news: {self.title}"


# ============================================================================
# Panel Discussion Models (Read-only from RDS)
# ============================================================================

class PanelDiscussion(models.Model):
    """Panel discussion results (read-only from RDS)"""

    class Meta:
        managed = False  # Django does not manage this table
        db_table = 'panel_discussions'
        ordering = ['-discussion_date', '-id']

    class MoodChoices(models.TextChoices):
        HAPPY = 'happy', 'Happy'
        NEUTRAL = 'neutral', 'Neutral'
        SAD = 'sad', 'Sad'

    country_code = models.CharField(max_length=10)
    topic = models.TextField()
    final_mood = models.CharField(max_length=20, choices=MoodChoices.choices)
    final_score = models.DecimalField(max_digits=5, decimal_places=2)
    introduction = models.TextField(blank=True, null=True)
    conclusion = models.TextField(blank=True, null=True)
    discussion_date = models.DateField()
    total_turns = models.IntegerField(null=True)
    debate_rounds = models.IntegerField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"{self.country_code} - {self.discussion_date} ({self.final_mood})"


class PanelExpertAnalysis(models.Model):
    """Expert analysis from panel discussion (read-only)"""

    class Meta:
        managed = False
        db_table = 'panel_expert_analyses'
        ordering = ['round_number', 'id']

    discussion = models.ForeignKey(
        PanelDiscussion,
        on_delete=models.DO_NOTHING,
        related_name='analyses'
    )
    expert_role = models.CharField(max_length=50)
    analysis_text = models.TextField()
    round_number = models.IntegerField()
    created_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.expert_role} - Round {self.round_number}"


class PanelVote(models.Model):
    """Voting results from panel discussion (read-only)"""

    class Meta:
        managed = False
        db_table = 'panel_votes'

    discussion = models.ForeignKey(
        PanelDiscussion,
        on_delete=models.DO_NOTHING,
        related_name='votes'
    )
    expert_role = models.CharField(max_length=50)
    vote_mood = models.CharField(max_length=20)
    confidence = models.DecimalField(max_digits=5, decimal_places=2)
    reasoning = models.TextField(blank=True)
    created_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.expert_role}: {self.vote_mood} ({self.confidence}%)"


class PanelTranscript(models.Model):
    """Full conversation transcript (read-only)"""

    class Meta:
        managed = False
        db_table = 'panel_transcripts'
        ordering = ['turn_order']

    discussion = models.ForeignKey(
        PanelDiscussion,
        on_delete=models.DO_NOTHING,
        related_name='transcripts'
    )
    speaker = models.CharField(max_length=50)
    content = models.TextField()
    round_number = models.IntegerField(null=True)
    turn_order = models.IntegerField()
    created_at = models.DateTimeField()

    def __str__(self) -> str:
        return f"{self.speaker} (Turn {self.turn_order})"
