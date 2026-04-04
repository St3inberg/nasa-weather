"""Pytest configuration and fixtures"""

import pytest
import sys
import os


@pytest.fixture(scope="session")
def setup_environment():
    """Set up test environment"""
    os.environ["NASA_API_KEY"] = "test_api_key_12345"
    yield
    # Cleanup if needed
    if "NASA_API_KEY" in os.environ:
        del os.environ["NASA_API_KEY"]


@pytest.fixture
def mock_nasa_response():
    """Fixture providing mock NASA API response"""
    return {
        "av_t": {
            "av": -60.5,
            "mn": -75.2,
            "mx": -45.3,
        },
        "av_p": {
            "av": 620.5,
            "mn": 600.0,
            "mx": 640.0,
        },
        "av_ws": {
            "av": 5.2,
            "mn": 2.1,
            "mx": 8.9,
        },
        "wd": {
            "most_common": {
                "compass_point": "NW"
            }
        }
    }


@pytest.fixture
def invalid_api_responses():
    """Fixture providing various invalid API responses"""
    return [
        None,
        {},
        {"error": "Invalid API key"},
        {"av_t": None},
    ]
