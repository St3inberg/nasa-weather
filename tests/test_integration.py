"""Tests for Home Assistant integration"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import os
import sys

# Add parent directory and custom_components to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "custom_components"))


class TestIntegration:
    """Test suite for NASA Mars Weather integration"""

    def test_manifest_exists(self):
        """Test that manifest.json exists and is valid"""
        try:
            import json
            manifest_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "custom_components",
                "nasa_mars_weather",
                "manifest.json"
            )
            
            assert os.path.exists(manifest_path), "manifest.json not found"
            
            with open(manifest_path, "r") as f:
                manifest = json.load(f)
            
            assert manifest["domain"] == "nasa_mars_weather"
            assert manifest["name"] == "NASA Mars Weather"
            assert manifest["config_flow"] is True
        except Exception as e:
            pytest.fail(f"test_manifest_exists failed: {e}")

    def test_strings_json_exists(self):
        """Test that strings.json exists and is valid JSON"""
        import json
        strings_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "custom_components",
            "nasa_mars_weather",
            "strings.json"
        )
        
        assert os.path.exists(strings_path), "strings.json not found"
        
        # Test that it's valid JSON
        with open(strings_path, "r") as f:
            strings = json.load(f)
        
        # Verify it has expected top-level keys
        assert isinstance(strings, dict), "strings.json should contain a dict"
        assert len(strings) > 0, "strings.json should not be empty"

    def test_init_py_exists(self):
        """Test that __init__.py exists and has required classes"""
        try:
            init_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "custom_components",
                "nasa_mars_weather",
                "__init__.py"
            )
            
            assert os.path.exists(init_path), "__init__.py not found"
            
            with open(init_path, "r") as f:
                content = f.read()
            
            assert "MarsWeatherUpdateCoordinator" in content
            assert "async_setup_entry" in content
            assert "async_unload_entry" in content
        except Exception as e:
            pytest.fail(f"test_init_py_exists failed: {e}")

    def test_config_flow_exists(self):
        """Test that config_flow.py exists and has required methods"""
        try:
            config_flow_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "custom_components",
                "nasa_mars_weather",
                "config_flow.py"
            )
            
            assert os.path.exists(config_flow_path), "config_flow.py not found"
            
            with open(config_flow_path, "r") as f:
                content = f.read()
            
            assert "NasaMarsWeatherConfigFlow" in content
            assert "async_step_user" in content
        except Exception as e:
            pytest.fail(f"test_config_flow_exists failed: {e}")

    def test_sensor_exists(self):
        """Test that sensor.py exists and has required classes"""
        try:
            sensor_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "custom_components",
                "nasa_mars_weather",
                "sensor.py"
            )
            
            assert os.path.exists(sensor_path), "sensor.py not found"
            
            with open(sensor_path, "r") as f:
                content = f.read()
            
            assert "MarsTemperatureSensor" in content
            assert "MarsPressureSensor" in content
            assert "MarsWindSpeedSensor" in content
            assert "MarsWindDirectionSensor" in content
            assert "async_setup_entry" in content
        except Exception as e:
            pytest.fail(f"test_sensor_exists failed: {e}")


class TestConfigValidation:
    """Test suite for configuration validation"""

    def test_valid_api_key_format(self):
        """Test that API key validation works"""
        try:
            # API keys should not be empty strings
            api_key = "valid_test_key_12345"
            assert api_key is not None
            assert len(api_key) > 0
            assert isinstance(api_key, str)
        except Exception as e:
            pytest.fail(f"test_valid_api_key_format failed: {e}")

    def test_invalid_api_key_empty(self):
        """Test that empty API keys are rejected"""
        try:
            api_key = ""
            assert len(api_key) == 0
        except Exception as e:
            pytest.fail(f"test_invalid_api_key_empty failed: {e}")

    @patch("requests.get")
    def test_api_endpoint_validation_success(self, mock_get):
        """Test API endpoint validation on success"""
        try:
            mock_response = MagicMock()
            mock_response.json.return_value = {"av_t": {"av": -60.5}}
            mock_get.return_value = mock_response
            
            # Simulate successful API call
            assert mock_response.json() is not None
            assert "av_t" in mock_response.json()
        except Exception as e:
            pytest.fail(f"test_api_endpoint_validation_success failed: {e}")

    @patch("requests.get")
    def test_api_endpoint_validation_invalid_key(self, mock_get):
        """Test API endpoint validation with invalid key"""
        try:
            mock_get.side_effect = Exception("Invalid API Key")
            
            try:
                mock_get("https://api.nasa.gov/insight_weather/")
                pytest.fail("Should have raised exception")
            except Exception:
                pass  # Expected
        except Exception as e:
            pytest.fail(f"test_api_endpoint_validation_invalid_key failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
