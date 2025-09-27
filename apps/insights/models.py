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


class CountryWeatherTrend(models.Model):
    """Daily temperature forecast trend for the dashboard chart."""

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="weather_trends",
    )
    label = models.CharField(max_length=16)
    temperature = models.SmallIntegerField()

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.country.code.upper()} trend {self.label}"


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


class CountryInsightStat(models.Model):
    """Supplementary stats shown on the dashboard."""

    class Sentiment(models.TextChoices):
        POSITIVE = "positive", "Positive"
        NEUTRAL = "neutral", "Neutral"
        NEGATIVE = "negative", "Negative"

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="insight_stats",
    )
    label = models.CharField(max_length=128)
    value = models.CharField(max_length=64)
    change = models.CharField(max_length=64)
    sentiment = models.CharField(max_length=16, choices=Sentiment.choices)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.country.code.upper()} stat {self.label}"


class CountryAlert(models.Model):
    """Active alerts associated with a country."""

    class Level(models.TextChoices):
        INFO = "info", "Info"
        WATCH = "watch", "Watch"
        WARNING = "warning", "Warning"

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="alerts",
    )
    alert_type = models.CharField(max_length=64)
    level = models.CharField(max_length=16, choices=Level.choices)
    message = models.TextField()
    recommended_action = models.CharField(max_length=255)

    class Meta:
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.country.code.upper()} alert {self.alert_type}"
