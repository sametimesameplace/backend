import environ
import json
from http import client
from pathlib import Path
from socket import gaierror

from django.core.exceptions import ImproperlyConfigured


class MetaSingleton(type):
    """Metaclass to create singleton classes.
    Include 'metaclass=MetaSingleton' keyword to use."""
    _instance = None
    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


def get_nearest_city(lat: float, long: float) -> str:
    """Get the city closest to a given set of coordinates in a radius of 100mi.

    Args:
        lat (float): latitude
        long (float): longitude

    Returns:
        str: Name of the closest city to the given coordinates.
    """
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    env = environ.Env()
    environ.Env.read_env(str(BASE_DIR / ".env"))

    try:
        RAPID_API = env.str("RAPID_API")
    except ImproperlyConfigured:
        return None

    conn = client.HTTPSConnection("wft-geo-db.p.rapidapi.com", timeout=2)

    # we need a + in the url if the longitude is not negative
    if long < 0:
        glue = ""
    else:
        glue = "%2B"

    # https://rapidapi.com/blog/how-to-use-geodb-cities-api/
    url = ("/v1/geo/locations/"
           + str(lat)
           + glue
           + str(long)
           + "/nearbyCities?limit=1&radius=100"
    )
    headers = {
        "X-RapidAPI-Key": RAPID_API,
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }
    try:
        conn.request("GET", url, headers=headers)
    # prevent exception when internet connectivity is limited
    except (TimeoutError, gaierror):
        return None
    response = conn.getresponse()
    data = json.loads(response.read().decode())
    try:
        city = data["data"][0]["city"]
    except:
        city = None

    return city
