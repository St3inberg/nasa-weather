# Testing Guide

## Running Tests

### Run All Tests
```bash
# Set API key and run tests
export NASA_API_KEY="test_key"
python -m pytest tests/ -v

# Or use the test runner script
python run_tests.py
```

### Run Specific Test File
```bash
export NASA_API_KEY="test_key"
python -m pytest tests/test_fetch_mars_weather.py -v
python -m pytest tests/test_integration.py -v
```

### Run Specific Test
```bash
export NASA_API_KEY="test_key"
python -m pytest tests/test_fetch_mars_weather.py::TestFetchMarsWeather::test_fetch_mars_weather_success -v
```

### Run with Coverage
```bash
export NASA_API_KEY="test_key"
python -m pytest tests/ --cov=custom_components --cov=fetch_mars_weather -v
```

## Test Structure

### test_fetch_mars_weather.py (10 tests)
Tests for the standalone Mars weather fetcher script:

1. **test_fetch_mars_weather_success** - Success case with valid API response
2. **test_fetch_mars_weather_no_api_key** - Graceful handling when API key is missing
3. **test_fetch_mars_weather_connection_error** - Network connection error handling
4. **test_fetch_mars_weather_timeout** - Request timeout error handling
5. **test_parse_weather_data_valid** - Parsing valid weather data
6. **test_parse_weather_data_none** - Parsing None data
7. **test_parse_weather_data_missing_fields** - Parsing incomplete data
8. **test_parse_weather_data_empty_dict** - Parsing empty dictionary
9. **test_display_weather_valid** - Displaying valid weather data
10. **test_display_weather_none** - Displaying None weather data

### test_integration.py (9 tests)
Tests for the Home Assistant integration:

#### Integration Structure Tests
1. **test_manifest_exists** - Verifies manifest.json exists and is valid
2. **test_strings_json_exists** - Verifies strings.json exists and is valid
3. **test_init_py_exists** - Verifies __init__.py with required classes
4. **test_config_flow_exists** - Verifies config_flow.py with config step
5. **test_sensor_exists** - Verifies sensor.py with all sensor classes

#### Configuration Validation Tests
6. **test_valid_api_key_format** - Validates API key format
7. **test_invalid_api_key_empty** - Rejects empty API keys
8. **test_api_endpoint_validation_success** - Validates successful API calls
9. **test_api_endpoint_validation_invalid_key** - Handles invalid API keys

## Error Handling

All tests include comprehensive try/catch blocks:

```python
try:
    # Test code
    assert condition
except Exception as e:
    pytest.fail(f"Test failed: {e}")
```

## Mock Data

The `conftest.py` file provides reusable fixtures:

- **setup_environment** - Sets up test environment with API key
- **mock_nasa_response** - Mock NASA API response data
- **invalid_api_responses** - Various invalid API response scenarios

## Test Coverage

- API calls and error handling
- Network errors (connection, timeout)
- Data parsing and validation
- Missing/invalid data handling
- Integration file structure
- Configuration validation
- Output formatting

## Running Tests in CI/CD

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
export NASA_API_KEY="test_api_key"
python -m pytest tests/ -v --tb=short
```

## Test Results

```
============================= 19 passed in 0.18s ==============================

Tests Summary:
- 10 fetch_mars_weather tests: ✓ All passing
- 9 integration tests: ✓ All passing
- Error handling: ✓ All scenarios covered
- API validation: ✓ All scenarios covered
```
