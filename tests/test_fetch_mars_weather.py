"""Tests for fetch_mars_weather.py"""

import pytest
import os
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fetch_mars_weather import fetch_mars_weather, parse_weather_data, display_weather


class TestFetchMarsWeather:
    """Test suite for Mars weather fetching"""

    @patch.dict(os.environ, {"NASA_API_KEY": "test_api_key"})
    @patch("fetch_mars_weather.requests.get")
    def test_fetch_mars_weather_success(self, mock_get):
        """Test successful API call"""
        try:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                "av_t": {"av": -60.5, "mn": -75.2, "mx": -45.3},
                "av_p": {"av": 620.5, "mn": 600.0, "mx": 640.0},
                "av_ws": {"av": 5.2, "mn": 2.1, "mx": 8.9},
                "wd": {"most_common": {"compass_point": "NW"}},
            }
            mock_get.return_value = mock_response
            
            data = fetch_mars_weather()
            
            assert data is not None
            assert "av_t" in data
            assert data["av_t"]["av"] == -60.5
        except Exception as e:
            pytest.fail(f"fetch_mars_weather_success failed: {e}")

    @patch.dict(os.environ, {}, clear=True)
    def test_fetch_mars_weather_no_api_key(self):
        """Test that None is returned when API key is missing"""
        try:
            data = fetch_mars_weather()
            assert data is None
        except Exception as e:
            pytest.fail(f"test_fetch_mars_weather_no_api_key failed: {e}")

    @patch.dict(os.environ, {"NASA_API_KEY": "test_api_key"})
    @patch("fetch_mars_weather.requests.get")
    def test_fetch_mars_weather_connection_error(self, mock_get):
        """Test handling of connection errors"""
        try:
            import requests
            mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
            
            data = fetch_mars_weather()
            assert data is None
        except Exception as e:
            pytest.fail(f"test_fetch_mars_weather_connection_error failed: {e}")

    @patch.dict(os.environ, {"NASA_API_KEY": "test_api_key"})
    @patch("fetch_mars_weather.requests.get")
    def test_fetch_mars_weather_timeout(self, mock_get):
        """Test handling of timeout errors"""
        try:
            import requests
            mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
            
            data = fetch_mars_weather()
            assert data is None
        except Exception as e:
            pytest.fail(f"test_fetch_mars_weather_timeout failed: {e}")


class TestParseWeatherData:
    """Test suite for weather data parsing"""

    def test_parse_weather_data_valid(self):
        """Test parsing valid weather data"""
        try:
            data = {
                "av_t": {"av": -60.5, "mn": -75.2, "mx": -45.3},
                "av_p": {"av": 620.5, "mn": 600.0, "mx": 640.0},
                "av_ws": {"av": 5.2, "mn": 2.1, "mx": 8.9},
                "wd": {"most_common": {"compass_point": "NW"}},
            }
            
            weather = parse_weather_data(data)
            
            assert weather is not None
            assert weather["temperature"]["average"] == -60.5
            assert weather["pressure"]["average"] == 620.5
            assert weather["wind_speed"]["average"] == 5.2
            assert weather["wind_direction"] == "NW"
        except Exception as e:
            pytest.fail(f"test_parse_weather_data_valid failed: {e}")

    def test_parse_weather_data_none(self):
        """Test parsing None data"""
        try:
            weather = parse_weather_data(None)
            assert weather is None
        except Exception as e:
            pytest.fail(f"test_parse_weather_data_none failed: {e}")

    def test_parse_weather_data_missing_fields(self):
        """Test parsing data with missing fields"""
        try:
            data = {"av_t": {"av": -60.5}}
            
            weather = parse_weather_data(data)
            # Should still parse but with some None values
            assert weather is not None
            assert weather["temperature"]["average"] == -60.5
        except Exception as e:
            pytest.fail(f"test_parse_weather_data_missing_fields failed: {e}")

    def test_parse_weather_data_empty_dict(self):
        """Test parsing empty data dictionary"""
        try:
            weather = parse_weather_data({})
            assert weather is None
        except Exception as e:
            pytest.fail(f"test_parse_weather_data_empty_dict failed: {e}")


class TestDisplayWeather:
    """Test suite for weather display"""

    def test_display_weather_valid(self, capsys):
        """Test displaying valid weather data"""
        try:
            weather = {
                "timestamp": "2026-04-04T12:00:00",
                "temperature": {"average": -60.5, "min": -75.2, "max": -45.3},
                "pressure": {"average": 620.5, "min": 600.0, "max": 640.0},
                "wind_speed": {"average": 5.2, "min": 2.1, "max": 8.9},
                "wind_direction": "NW",
            }
            
            display_weather(weather)
            captured = capsys.readouterr()
            
            assert "MARS WEATHER DATA" in captured.out
            assert "-60.5" in captured.out
            assert "620.5" in captured.out
        except Exception as e:
            pytest.fail(f"test_display_weather_valid failed: {e}")

    def test_display_weather_none(self, capsys):
        """Test displaying None weather data"""
        try:
            display_weather(None)
            captured = capsys.readouterr()
            
            assert "No weather data available" in captured.out
        except Exception as e:
            pytest.fail(f"test_display_weather_none failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
