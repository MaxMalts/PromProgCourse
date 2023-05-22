import pytest
from weather_03.weather_wrapper import WeatherWrapper


def test_find_diff_two_cities(requests_mock):
    city1_name = 'city1'
    city2_name = 'city2'
    city1_temperature = 4.0
    city2_temperature = 10.0
    
    mock_today(requests_mock, city1_name, city1_temperature)
    mock_today(requests_mock, city2_name, city2_temperature)
    
    assert city1_temperature - city2_temperature == WeatherWrapper('api-key').find_diff_two_cities(city1_name, city2_name)

def test_get_diff_string_colder(requests_mock):
    city1_name = 'city1'
    city2_name = 'city2'
    city1_temperature = 4.0
    city2_temperature = 10.0
    
    mock_today(requests_mock, city1_name, city1_temperature)
    mock_today(requests_mock, city2_name, city2_temperature)
    
    expected = f'Weather in {city1_name} is colder than in {city2_name} by {int(city2_temperature - city1_temperature)} degrees'
    assert expected == WeatherWrapper('api-key').get_diff_string(city1_name, city2_name)
    
def test_get_diff_string_warmer(requests_mock):
    city1_name = 'city1'
    city2_name = 'city2'
    city1_temperature = 10.0
    city2_temperature = 4.0
    
    mock_today(requests_mock, city1_name, city1_temperature)
    mock_today(requests_mock, city2_name, city2_temperature)
    
    expected = f'Weather in {city1_name} is warmer than in {city2_name} by {int(city1_temperature - city2_temperature)} degrees'
    assert expected == WeatherWrapper('api-key').get_diff_string(city1_name, city2_name)

def test_get_tomorrow_diff_much_warmer(requests_mock):
    city_name = 'city'
    temperature = 4.0
    tomorrow_temperature = 10.0
    
    mock_today(requests_mock, city_name, temperature)
    mock_tomorrow(requests_mock, city_name, tomorrow_temperature)
    
    expected = f'The weather in {city_name} tomorrow will be much warmer than today' 
    assert expected == WeatherWrapper('api-key').get_tomorrow_diff(city_name)

def test_get_tomorrow_diff_warmer(requests_mock):
    city_name = 'city'
    temperature = 4.0
    tomorrow_temperature = 5.0
    
        
    mock_today(requests_mock, city_name, temperature)
    mock_tomorrow(requests_mock, city_name, tomorrow_temperature)
    
    expected = f'The weather in {city_name} tomorrow will be warmer than today' 
    assert expected == WeatherWrapper('api-key').get_tomorrow_diff(city_name)
    
def test_get_tomorrow_diff_much_colder(requests_mock):
    city_name = 'city'
    temperature = 4.0
    tomorrow_temperature = 0.0
    
    mock_today(requests_mock, city_name, temperature)
    mock_tomorrow(requests_mock, city_name, tomorrow_temperature)
    
    expected = f'The weather in {city_name} tomorrow will be much colder than today' 
    assert expected == WeatherWrapper('api-key').get_tomorrow_diff(city_name)
    
def test_get_tomorrow_diff_colder(requests_mock):
    city_name = 'city'
    temperature = 4.0
    tomorrow_temperature = 3.0
    
    mock_today(requests_mock, city_name, temperature)
    mock_tomorrow(requests_mock, city_name, tomorrow_temperature)
    
    expected = f'The weather in {city_name} tomorrow will be colder than today' 
    assert expected == WeatherWrapper('api-key').get_tomorrow_diff(city_name)
    
def test_get_tomorrow_diff_same(requests_mock):
    city_name = 'city'
    temperature = 4.0
    tomorrow_temperature = 4.3
    
    mock_today(requests_mock, city_name, temperature)
    mock_tomorrow(requests_mock, city_name, tomorrow_temperature)
    
    expected = f'The weather in {city_name} tomorrow will be the same than today' 
    assert expected == WeatherWrapper('api-key').get_tomorrow_diff(city_name)
    
def test_get_response_city_error(requests_mock):
    city_name = 'city'
    requests_mock.get(f'http://api.openweathermap.org/data/2.5/weather?q={city_name}',
                      status_code = 500)
    with pytest.raises(AttributeError):
        WeatherWrapper('api-key').get_response_city(city_name, 'http://api.openweathermap.org/data/2.5/weather')
    
def mock_today(requests_mock, city_name, temperature):
    requests_mock.get(f'http://api.openweathermap.org/data/2.5/weather?q={city_name}',
                      json={'main': {'temp': temperature}})

def mock_tomorrow(requests_mock, city_name, temperature):
    requests_mock.get(f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}',
                      json={'list': [None, None, None, None, None, None, None, {'main': {'temp': temperature}}]})