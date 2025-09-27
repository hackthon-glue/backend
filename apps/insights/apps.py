"""App configuration for insights."""
from __future__ import annotations

from django.apps import AppConfig


class InsightsConfig(AppConfig):
    """Configuration for the insights app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.insights"
    verbose_name = "Insights"
