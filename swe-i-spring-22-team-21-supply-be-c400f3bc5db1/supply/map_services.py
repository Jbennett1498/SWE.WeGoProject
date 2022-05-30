import requests

base_url = 'https://api.mapbox.com'
access_token = 'pk.eyJ1IjoidGdyYXUiLCJhIjoiY2t6YTRyaHlmMGVlcDJvczhkZWJvd3g0dSJ9.ihqqYGiq6MIHVpJd_7gkJg'


def get_durations_matrix(coordinates, destinations, sources, profile='mapbox/driving'):
    url = f'{base_url}/directions-matrix/v1/{profile}/{coordinates}'
    params = {
        'destinations': destinations,
        'sources': sources,
        'access_token': access_token
    }
    return requests.get(url, params=params).json()


def get_route(coordinates, profile='mapbox/driving'):
    url = f'{base_url}/directions/v5/{profile}/{coordinates}'
    params = {
        'access_token': access_token
    }
    return requests.get(url, params=params).json()
