"""Management command to seed demo data for country insights."""
from __future__ import annotations

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.insights.data.demo import COUNTRIES
from apps.insights.models import (
    Country,
    CountryAlert,
    CountryInsightStat,
    CountryNewsItem,
    CountrySentiment,
    CountrySummary,
    CountryWeather,
    CountryWeatherTrend,
)


class Command(BaseCommand):
    """Seed the database with a curated set of demo countries."""

    help = "Populate the insights tables with demo data mirroring the frontend mocks."

    def handle(self, *_args, **_options) -> None:
        with transaction.atomic():
            for entry in COUNTRIES:
                summary_data = entry["summary"]
                insights = entry["insights"]

                country, _ = Country.objects.update_or_create(
                    code=entry["code"],
                    defaults={
                        "name": entry["name"],
                        "latitude": Decimal(str(entry["lat"])),
                        "longitude": Decimal(str(entry["lng"])),
                    },
                )

                CountrySummary.objects.update_or_create(
                    country=country,
                    defaults={
                        "headline": summary_data["headline"],
                        "weather": summary_data["weather"],
                        "persona": summary_data["persona"],
                        "mood_narrative": summary_data["moodNarrative"],
                        "today_summary": summary_data["todaySummary"],
                    },
                )

                weather_now = insights["weatherNow"]
                CountryWeather.objects.update_or_create(
                    country=country,
                    defaults={
                        "condition": weather_now["condition"],
                        "temperature": weather_now["temperature"],
                        "feels_like": weather_now["feelsLike"],
                        "humidity": weather_now["humidity"],
                        "wind": weather_now["wind"],
                        "precipitation_chance": weather_now["precipitationChance"],
                    },
                )

                CountrySentiment.objects.filter(country=country).delete()
                CountrySentiment.objects.bulk_create(
                    [
                        CountrySentiment(
                            country=country,
                            label=point["label"],
                            score=point["score"],
                        )
                        for point in insights["sentiment"]
                    ]
                )

                CountryWeatherTrend.objects.filter(country=country).delete()
                CountryWeatherTrend.objects.bulk_create(
                    [
                        CountryWeatherTrend(
                            country=country,
                            label=point["label"],
                            temperature=point["temperature"],
                        )
                        for point in insights["weatherTrend"]
                    ]
                )

                CountryNewsItem.objects.filter(country=country).delete()
                CountryNewsItem.objects.bulk_create(
                    [
                        CountryNewsItem(
                            country=country,
                            title=item["title"],
                            summary=item["summary"],
                            url=item["url"],
                            category=item["category"],
                            tone=item["tone"],
                        )
                        for item in insights["news"]
                    ]
                )

                CountryInsightStat.objects.filter(country=country).delete()
                CountryInsightStat.objects.bulk_create(
                    [
                        CountryInsightStat(
                            country=country,
                            label=stat["label"],
                            value=stat["value"],
                            change=stat["change"],
                            sentiment=stat["sentiment"],
                        )
                        for stat in insights["stats"]
                    ]
                )

                CountryAlert.objects.filter(country=country).delete()
                CountryAlert.objects.bulk_create(
                    [
                        CountryAlert(
                            country=country,
                            alert_type=alert["type"],
                            level=alert["level"],
                            message=alert["message"],
                            recommended_action=alert["recommendedAction"],
                        )
                        for alert in insights["alerts"]
                    ]
                )

        self.stdout.write(self.style.SUCCESS("Demo insights data loaded."))
