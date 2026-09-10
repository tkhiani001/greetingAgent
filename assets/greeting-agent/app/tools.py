"""Greeting agent tools: time-of-day detection and greeting generation."""

import logging
from datetime import datetime, timezone

from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def get_time_of_day() -> str:
    """Detect the current time of day and return one of: 'morning', 'afternoon', or 'evening'.

    Uses server-side UTC time. Classification:
    - morning:   00:00 – 11:59
    - afternoon: 12:00 – 17:59
    - evening:   18:00 – 23:59

    Returns:
        str: One of 'morning', 'afternoon', 'evening', or 'day' as fallback.
    """
    try:
        hour = datetime.now(tz=timezone.utc).hour
        if 0 <= hour < 12:
            return "morning"
        elif 12 <= hour < 18:
            return "afternoon"
        else:
            return "evening"
    except Exception:
        logger.exception("Time detection failed, returning fallback 'day'")
        return "day"


@tool
def get_greeting(time_of_day: str) -> str:
    """Return a polite greeting based on the time of day.

    Args:
        time_of_day: One of 'morning', 'afternoon', 'evening', or 'day' (fallback).

    Returns:
        str: A polite, time-appropriate greeting message.
    """
    greetings = {
        "morning": "Good morning! Welcome back. Hope you have a great day ahead.",
        "afternoon": "Good afternoon! Welcome back. Hope your day is going well.",
        "evening": "Good evening! Welcome back. Hope you had a productive day.",
    }
    greeting = greetings.get(time_of_day, "Hello! Welcome back.")
    if not greeting:
        greeting = "Hello! Welcome back."
    return greeting
