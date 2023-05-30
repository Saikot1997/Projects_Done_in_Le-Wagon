# pylint: disable=missing-module-docstring

import sys
import urllib.parse
import requests

BASE_URI = "https://weather.lewagon.com"



def search_city(query):
    '''
    Look for a given city. If multiple options are returned, have the user choose between them.
    Return one city (or None)
    '''
    response = requests.get(BASE_URI).json()
    forecast_url= response["endpoints"][0]["base_url"]
    a=1
    city_info = requests.get(forecast_url,params={'q': query,'limit' : 5}).json()
    if len(city_info) == 0:
        return None
    if query != city_info[0]["name"]:
        for city in city_info:
            print(str(a) +". " + city["name"] +"," + city["country"])
            a+=1
        b = input("Multiple matches found, which city did you mean?\n")
        c=b-1
        return city_info[c]
    return city_info[0]



def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''
    response = requests.get(BASE_URI).json()
    forecast_url= response["endpoints"][2]["base_url"]
    forcast_info = requests.get(forecast_url,params={'lat': lat,'lon' : lon}).json()


    return forcast_info["list"]

def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    info = search_city(query)

    # TODO: Display weather forecast for a given city
    lat = info["lat"]
    lon = info["lon"]

    next_five = weather_forecast(lat, lon)
    dtext= weather[0]["dt_txt"]
    a = "null"
    for weather in weather:
        if weather["dt_txt"][0:10] != a:
            print(weather["dt_txt"][0:10] + " " + weather["weather"][0]["main"] + " (" + str(round(weather["main"]["temp"]-273.15)) + "°C)")
            a = weather["dt_txt"][0:10]


if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
