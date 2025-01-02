# adapted from https://pypi.org/project/vehicle-makes/
import requests
from requests_futures.sessions import FuturesSession

_BASE_URI = 'https://www.autotrader.co.uk'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

def _get_makes():
    url = f'{_BASE_URI}/json/search/options?advertising-location=at_cars'
    resp = requests.get(url,headers=headers)
    resp.raise_for_status()
    return (r['displayName'] for r in resp.json()['options']['make'])


def get_makes_and_models():
    session = FuturesSession()
    futures = []
    for make in _get_makes():
        url = f'{_BASE_URI}/json/search/options?make={make}'
        futures.append((make, session.get(url,headers=headers)))

    makes_and_models = {}
    responses = ((m, f.result()) for m, f in futures)
    for make, response in responses:
        models = tuple(
            r['displayName'] for r in response.json()['options']['model']
        )
        makes_and_models[make] = models
    return makes_and_models