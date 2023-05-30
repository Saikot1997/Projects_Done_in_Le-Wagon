# pylint: disable=no-value-for-parameter
"""
Client of the Wagon OpenGraph API
"""
# To manually test, please uncomment the following lines and run `python opengraph.py`:
#mport pprint
import requests


def fetch_metadata(url):
    """
    Return a dictionary of OpenGraph metadata found in HTML of given url
    """
    try:
        URL = f"https://opengraph.lewagon.com/?url={url}"
        info = requests.get(URL).json()
        return info["data"]
    except:
      return {}

#pp = pprint.PrettyPrinter(indent=4)pp.pprint(fetch_metadata("https://www.github.com"))
