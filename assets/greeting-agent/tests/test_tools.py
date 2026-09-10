"""Unit tests for greeting agent tools."""

from unittest.mock import MagicMock, patch
from datetime import datetime, timezone

import pytest


class TestGetTimeOfDay:
    """Tests for get_time_of_day tool."""

    def _call_tool(self):
        from tools import get_time_of_day
        return get_time_of_day.invoke({})

    def test_morning_returns_morning(self):
        mock_dt = MagicMock()
        mock_dt.hour = 9  # 9 AM
        with patch("tools.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_dt
            result = self._call_tool()
        assert result == "morning"

    def test_midnight_returns_morning(self):
        mock_dt = MagicMock()
        mock_dt.hour = 0  # 12 AM
        with patch("tools.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_dt
            result = self._call_tool()
        assert result == "morning"

    def test_noon_returns_afternoon(self):
        mock_dt = MagicMock()
        mock_dt.hour = 12  # 12 PM
        with patch("tools.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_dt
            result = self._call_tool()
        assert result == "afternoon"

    def test_afternoon_returns_afternoon(self):
        mock_dt = MagicMock()
        mock_dt.hour = 15  # 3 PM
        with patch("tools.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_dt
            result = self._call_tool()
        assert result == "afternoon"

    def test_evening_start_returns_evening(self):
        mock_dt = MagicMock()
        mock_dt.hour = 18  # 6 PM
        with patch("tools.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_dt
            result = self._call_tool()
        assert result == "evening"

    def test_late_night_returns_evening(self):
        mock_dt = MagicMock()
        mock_dt.hour = 23  # 11 PM
        with patch("tools.datetime") as mock_datetime:
            mock_datetime.now.return_value = mock_dt
            result = self._call_tool()
        assert result == "evening"

    def test_exception_returns_day_fallback(self):
        with patch("tools.datetime") as mock_datetime:
            mock_datetime.now.side_effect = Exception("clock error")
            result = self._call_tool()
        assert result == "day"


class TestGetGreeting:
    """Tests for get_greeting tool."""

    def _call_tool(self, time_of_day: str):
        from tools import get_greeting
        return get_greeting.invoke({"time_of_day": time_of_day})

    def test_morning_greeting(self):
        result = self._call_tool("morning")
        assert "morning" in result.lower()
        assert len(result) > 0

    def test_afternoon_greeting(self):
        result = self._call_tool("afternoon")
        assert "afternoon" in result.lower()
        assert len(result) > 0

    def test_evening_greeting(self):
        result = self._call_tool("evening")
        assert "evening" in result.lower()
        assert len(result) > 0

    def test_fallback_greeting(self):
        result = self._call_tool("day")
        assert len(result) > 0
        assert "hello" in result.lower() or "welcome" in result.lower()

    def test_unknown_value_returns_fallback(self):
        result = self._call_tool("unknown-time")
        assert len(result) > 0

    def test_greeting_is_polite(self):
        for time_of_day in ["morning", "afternoon", "evening"]:
            result = self._call_tool(time_of_day)
            assert any(word in result.lower() for word in ["welcome", "hope", "good"])
