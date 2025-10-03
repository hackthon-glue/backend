"""Management command to seed demo data for country insights."""
from __future__ import annotations

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.insights.data.demo import COUNTRIES
from apps.insights.models import (
    Country,
    CountryNewsItem,
    CountrySentiment,
    CountrySummary,
    CountryWeather,
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

        self.stdout.write(self.style.SUCCESS("Demo insights data loaded."))
