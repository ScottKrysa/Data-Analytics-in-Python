"""
Assignment 2: Google Geocoding

This returns address, lat, and long of stores or other locations in a specified country.
Must input your own google API key.
"""

import my_google_keys

region_codes = dict()
region_codes["United States"] = "US"
region_codes["United Kingdom"] = "UK"
region_codes["Spain"] = "ES"
region_codes["Canada"] = "CA"
region_codes["China"] = "CN"
region_codes["Japan"] = "JP"

#Helper function that returns True if the country in the result matches the country parameter
def match_country(address_components,country):
    for item in address_components:
        if "country" in item['types']:
            return item['long_name'] == country
    return False

#A function that, given a response from google's geocoding api, returns a list of results
# containing (address, lat, lng) tuples
def get_json_data(response,country):
    json_data = response.json()
    result_list = list()
    for result in json_data['results']:
        formatted_address = result['formatted_address']
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']
        address_components = result['address_components']
        if match_country(address_components,country):
            result_list.append((formatted_address,lat,lng))
        else:
            break
    return result_list
    
def get_geolocation_data(address_string,country,format="JSON"):
    import json
    import requests
    result = None #Compute the desired json string and replace this. Leave as None if the process fails
    
    google_api_key =  my_google_keys.google_api_key ##Enter API Key here
    address_url = address_string.replace(" ","+")
    country_region = region_codes[country]
    
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&region=%s&key=%s" %(address_string, country_region, google_api_key)
    # url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s?%s&key=%s" %(address_string, country, google_api_key)

    try:
        response = requests.get(url)
        if not response.status_code == 200:
            return None
        else:
            try:
                response_data = response.json()
            except:
                return None
    except:
        return None

    try:
        get_json_data(response, country)
        result = get_json_data(response, country)
    except:
        return None

    return result
    

print(get_geolocation_data("Prada",country='Spain',format='json'))
