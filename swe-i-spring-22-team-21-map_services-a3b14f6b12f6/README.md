## Map Services goals:
# Map services (MS) is expected to be used in a few ways:
# 1- Generate maps for the customer to view where they are and where they are going. This can be done at the time of order, or during the transportation.
# 2- Generate address information from coordinates generated from the user or the vehicle, or coordinates from the address information given by the customer for their destination.
# 3- Generate routing information for the autonomous vehicles to follow, and visualise for the customer to see their route from origin to destination. 

We are using Mapbox for our MS, and their API documentation is robust and useful.
https://docs.mapbox.com/

# Mapbox API Calls
## Below are a series of python calls to our MS for different API URIs. Versions of these will be able to be inserted into both our supply and demand cloud servers as required


# MAP SERVICES

## Rendering Maps
### GET: Map of Austin, TX
import http.client

conn = http.client.HTTPSConnection("api.mapbox.com")
payload = ''
headers = {}
conn.request("GET", "/styles/v1/mapbox/streets-v11/static/-97.7368,30.3361,8.28,0/400x400?access_token=pk.eyJ1IjoidGdyYXUiLCJhIjoiY2t6YTRyaHlmMGVlcDJvczhkZWJvd3g0dSJ9.ihqqYGiq6MIHVpJd_7gkJg", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


### GET: Map of St. Edward's with a pin
import http.client

conn = http.client.HTTPSConnection("api.mapbox.com")
payload = ''
headers = {}
conn.request("GET", "/styles/v1/mapbox/light-v10/static/pin-s-e+000(-97.754283,30.228176)/-97.754283,30.228176,12/500x300?access_token=pk.eyJ1IjoidGdyYXUiLCJhIjoiY2t6YTRyaHlmMGVlcDJvczhkZWJvd3g0dSJ9.ihqqYGiq6MIHVpJd_7gkJg", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


## DIRECTIONS:
### Get: directions from St Edwards to Gus' Fried Chicken:
import http.client

conn = http.client.HTTPSConnection("api.mapbox.com")
payload = ''
headers = {}
conn.request("GET", "/directions/v5/mapbox/driving/-97.754283,30.228176;-97.741621,30.263619?access_token=pk.eyJ1IjoidGdyYXUiLCJhIjoiY2t6YTRyaHlmMGVlcDJvczhkZWJvd3g0dSJ9.ihqqYGiq6MIHVpJd_7gkJg", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


## GEOLOCATION:
### Get: Coordinates to Address
import http.client

conn = http.client.HTTPSConnection("api.mapbox.com")
payload = ''
headers = {}
conn.request("GET", "/geocoding/v5/mapbox.places/-73.98395997944657,40.76321913507897.json?types=place%252Cpostcode%252Caddress&limit=1&access_token=pk.eyJ1IjoidGdyYXUiLCJhIjoiY2t6YTRyaHlmMGVlcDJvczhkZWJvd3g0dSJ9.ihqqYGiq6MIHVpJd_7gkJg", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))