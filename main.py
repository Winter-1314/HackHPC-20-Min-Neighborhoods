import os
import googlemaps

RADIUS = [10000,1600]
ACTIONS = ["Y","N"]
API_KEY = (os.getenv("API_KEY"))
MODE_OF_TRANS = ["driving", "walking", "bicycling", "transit"]
FIND_PLACE_TEXTQUERY = "textquery"
FIND_PLACE_PHONENUMBER = "phonenumber"
PLACE_ID = "place_id"
ADDRESS_COMMA = ["locality", "route"]
ADDRESS_NEWLINE = ["point_of_interest", "establishment"]
ADDRESS_IGNORE = ["administrative_area_level_2", "administrative_area_level_3"]
gmaps = googlemaps.Client(key=API_KEY)


def collectInfo():
    # First Collect Address From User - Input
    num_of_attept = 0
    correct_location = False
    while correct_location != True:
        list_of_locations = []
        if num_of_attept > 0:
            print("Please enter a more detailed address.")
        search_place = input("Please enter a name, address, or phone number as your starting location:\n") 
        origin_location = gmaps.find_place(input=search_place, input_type=FIND_PLACE_TEXTQUERY)
        origin_location_status = origin_location.get("status")
        while(origin_location_status != "OK"):
                search_place = input("Invaild Location!\nPlease enter a name, address, or phone number as your starting location:\n")
                origin_location = gmaps.find_place(input=search_place, input_type=FIND_PLACE_TEXTQUERY)
                origin_location_status = origin_location.get("status")
        origin_location_place_id = origin_location.get("candidates")
        for places in origin_location_place_id:
            location_data = gmaps.place(place_id=places.get(PLACE_ID))
            location_address = location_data.get("result").get("address_components")
            address_string = ""
            for parts in location_address:
                type_address = parts.get("types")[0]
                if type_address in ADDRESS_IGNORE:
                    continue
                elif type_address in ADDRESS_NEWLINE:
                    address_string = address_string + " " + parts.get("long_name") + "\n"
                elif type_address in ADDRESS_COMMA:
                    address_string = address_string + " " + parts.get("long_name")+","
                else:
                    address_string = address_string + " " + parts.get("long_name")
            list_of_locations.append(address_string)
        temp = input(f"Is this address below your address?(Y/N):\n{list_of_locations[0]}\n")
        while temp.upper() not in ACTIONS:
            temp = input("Please enter Y for Yes and N for no (Y/N):\n")
        if temp.upper() == "Y":
            correct_location = True
        num_of_attept += 1
    return list_of_locations[0]    
    
def getGeoCode(address):
    # Convert User Collected Address to Lat and Long - geocode()
    location_geocode = gmaps.geocode(address=address)
    lat = location_geocode[0].get("geometry").get("location").get("lat")
    long = location_geocode[0].get("geometry").get("location").get("lng")
    lat_long_lst = [lat,long]
    return lat_long_lst

def serechForPlaces(lat_long, radius ,type=None):
    # Serech for places near an address in a radius and type - places_nearby()
    location_dict = {}
    if type == None:
        search_info = gmaps.places_nearby(location=lat_long, radius=radius)
    else:
        search_info = gmaps.places_nearby(location=lat_long, radius=radius, type=type)
    search_result = search_info.get("results")
    for index in search_result:
        location_dict[index.get("name")] = {}
        location_dict[index.get("name")]["status"] = index.get("business_status")
        location_dict[index.get("name")]["place_id"] = index.get("place_id")
        location_dict[index.get("name")]["rating"] = index.get("rating")
        location_dict[index.get("name")]["lat"] = index.get("geometry").get("location").get("lat")
        location_dict[index.get("name")]["lng"] = index.get("geometry").get("location").get("lng")
        location_dict[index.get("name")]["classification"] = index.get("types")
        location_dict[index.get("name")]["price_lvl"] = index.get("price_level")
        location_dict[index.get("name")]["pull_address"] = index.get("vicinity")
    return location_dict

def displayPlaces(list_of_location):
    for location in list_of_location:
        print(f"{location}:")
        for item in list_of_location[location]:
            print(f"{item}:{list_of_location[location][item]}")
        print(f'\n{"*":*^25}\n')

def makeListofLocationAddress(locations_dict):
    # Convert the list of location to list of addresses - reverse_geocode()
    for location in locations_dict:
        locations_dict[location]["address"] = gmaps.reverse_geocode(latlng=locations_dict[location]["place_id"])[0].get("formatted_address")

                                                                    
def computeDistance(locations_dict, origin, mode="walking"):
    # Make a list of Matrix for each type of transportation - distance_matrix()
    for location in locations_dict:
        locations_dict[location]["travel_time"] = gmaps.distance_matrix(origins=origin,destinations=locations_dict[location].get("address"),mode=mode).get("rows")[0].get("elements")[0].get("duration").get("text")
    
if __name__ == '__main__':
    origin_location = collectInfo()
    locations_dict = serechForPlaces(getGeoCode(origin_location), RADIUS[1])
    makeListofLocationAddress(locations_dict)
    computeDistance(locations_dict, origin_location, MODE_OF_TRANS[1])
    displayPlaces(locations_dict)
