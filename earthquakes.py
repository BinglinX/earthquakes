import requests
import json

def get_data():
 
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"}
    )


    text = response.text

    # Data is in json format, so directly load text with json.loads
    # After loaded, the data has 4 keys: type, metadata, features, and bbox
    # Information about each earthquake is stroe in features, which is a list of dictionaries
    # Each dictionary is an earthquake

    data = json.loads(text)['features']
  
    return data

def count_earthquakes(data):
    """Get the total number of earthquakes in the response."""
    return len(data)


def get_magnitude(earthquake):
    """Retrive the magnitude of an earthquake item."""
    return earthquake['properties']['mag']


def get_location(earthquake):
    """Retrieve the latitude and longitude of an earthquake item."""
    # There are three coordinates, but we don't care about the third (altitude)
    return earthquake['geometry']['coordinates'][0:2]


def get_maximum(data):
    """Get the magnitude and location of the strongest earthquake in the data."""
    max_mag = 0
    max_coord = [0,0]

    # Each i is an earthquake so the above functions can be used
    for i in data:
        mag = get_magnitude(i)
        coord = get_location(i)

        # If the current magnitude is larger than any of the earthquake, update the maximum
        if mag>max_mag:
            max_mag = mag
            max_coord = coord

    return(max_mag,max_coord)



# With all the above functions defined, we can now call them and get the result
if __name__ == 'main':
    data = get_data()
    print(f"Loaded {count_earthquakes(data)}")
    max_magnitude, max_location = get_maximum(data)
    print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}")