import os
import googlemaps
# Planned on using this for graphing of the data
import gmaps

RADIUS = [10000, 1000, 1600, 2000]
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


def collectInfo() -> str:
    """
    Collects the address of the location that the user is looking for.
    :return: The address of the location the user entered
    :rtype: str
    """
    # First Collect Address From User - Input
    num_of_attept = 0
    correct_location = False
    while correct_location != True:
        list_of_locations = []
        if num_of_attept > 0:
            print("Please enter a more detailed address.")
        search_place = input(
            "Please enter a name, address, or phone number as your starting location:\n"
        )
        origin_location = gomaps.find_place(input=search_place,
                                            input_type=FIND_PLACE_TEXTQUERY)
        origin_location_status = origin_location.get("status")
        while (origin_location_status != "OK"):
            search_place = input(
                "Invaild Location!\nPlease enter a name, address, or phone number as your starting location:\n"
            )
            origin_location = gomaps.find_place(
                input=search_place, input_type=FIND_PLACE_TEXTQUERY)
            origin_location_status = origin_location.get("status")
        origin_location_place_id = origin_location.get("candidates")
        for places in origin_location_place_id:
            location_data = gomaps.place(place_id=places.get(PLACE_ID))
            location_address = location_data.get("result").get(
                "address_components")
            address_string = ""
            for parts in location_address:
                type_address = parts.get("types")[0]
                if type_address in ADDRESS_IGNORE:
                    continue
                elif type_address in ADDRESS_NEWLINE:
                    address_string = address_string + " " + parts.get(
                        "long_name") + "\n"
                elif type_address in ADDRESS_COMMA:
                    address_string = address_string + " " + parts.get(
                        "long_name") + ","
                else:
                    address_string = address_string + " " + parts.get(
                        "long_name")
            list_of_locations.append(address_string)
        temp = input(
            f"Is this address below your address?(Y/N):\n{list_of_locations[0]}\n"
        )
        while temp.upper() not in ACTIONS:
            temp = input("Please enter Y for Yes and N for no (Y/N):\n")
        if temp.upper() == "Y":
            correct_location = True
        num_of_attept += 1
    return list_of_locations[0]


def collectTransportation() -> int:
    """
    Collects the type of transportion that the data is going to be calculated for
    :return: The number that correspondes to the type of transportation
    :rtype: int
    """
    # Secondly, Collects Transportation Method From User - Input
    type_of_trans = input(
        f"What type of transportation do you want to use?\n\t1.{MODE_OF_TRANS[0]}\n\t2.{MODE_OF_TRANS[1]}\n\t3.{MODE_OF_TRANS[2]}\n\t4.{MODE_OF_TRANS[3]}\nPlease enter a number between 1-4:\n"
    )
    while int(type_of_trans) not in [1, 2, 3, 4]:
        print("Please make sure you enter a number is and that is between 1-4")
        type_of_trans = input(
            f"What type of transportation do you want to use?\n\t1.{MODE_OF_TRANS[0]}\n\t2.{MODE_OF_TRANS[1]}\n\t3.{MODE_OF_TRANS[2]}\n\t4.{MODE_OF_TRANS[3]}\nPlease enter a number between 1-4:\n"
        )
    return int(type_of_trans) - 1


def getGeoCode(address: str) -> list:
    """
    Given address get GeoCode that includes the lat and long version of that address
    :param address: The address we want to get the GeoCode
    :type address: str
    :return: The long and lat in list format
    :rtype: list
    """
    # Convert User Collected Address to Lat and Long - geocode()
    location_geocode = gomaps.geocode(address=address)
    lat = location_geocode[0].get("geometry").get("location").get("lat")
    long = location_geocode[0].get("geometry").get("location").get("lng")
    lat_long_lst = [lat, long]
    return lat_long_lst


def serechForPlaces(lat_long: list, radius: int, type: str = None) -> dict:
    """
    Computes all the locations that are near the address provided as a lat/long
    :param lat_long: List version of the lat and long
    :type lat_long: list
    :param radius: The radius that we want to search from the lat and long
    :type radius: int
    :param type: Any specific type of location we want to look for
    :type type: str
    :return: A dictionary with all the locations nearby
    :rtype: dict
    """
    # Serech for places near an address in a radius and type - places_nearby()
    location_dict = {}
    if type == None:
        search_info = gomaps.places_nearby(location=lat_long, radius=radius)
    else:
        search_info = gomaps.places_nearby(location=lat_long,
                                           radius=radius,
                                           type=type)
    search_result = search_info.get("results")
    for index in search_result:
        location_dict[index.get("name")] = {}
        location_dict[index.get("name")]["status"] = index.get(
            "business_status")
        location_dict[index.get("name")]["place_id"] = index.get("place_id")
        location_dict[index.get("name")]["rating"] = index.get("rating")
        location_dict[index.get("name")]["lat"] = index.get("geometry").get(
            "location").get("lat")
        location_dict[index.get("name")]["lng"] = index.get("geometry").get(
            "location").get("lng")
        location_dict[index.get("name")]["classification"] = index.get("types")
        location_dict[index.get("name")]["price_lvl"] = index.get(
            "price_level")
        location_dict[index.get("name")]["pull_address"] = index.get(
            "vicinity")
    return location_dict


def displayPlaces(dict_of_location: dict) -> None:
    """
    Given a list of location display it in a nicely readable format
    :param dict_of_location: A dictionary with all the locations nearby
    :type dict_of_location: dict
    :return: None
    :rtype: None
    """
    # Neatly Display The List Of Locations within 20 Minutes Of the Users Input Location And Transportation Method
    for location in dict_of_location:
        print(f"{location}:")
        for item in dict_of_location[location]:
            print(f"{item}:{dict_of_location[location][item]}")
        print(f'\n{"*":*^25}\n')


def addLocationAddressData(locations_dict: dict) -> None:
    """
    Given a dictionary of all location add their address to the dict
    :param locations_dict: A dictionary with all the locations nearby
    :type locations_dict: dict
    :return: None
    :rtype: None
    """
    # Convert the list of location to list of addresses - reverse_geocode()
    for location in locations_dict:
        locations_dict[location]["address"] = gomaps.reverse_geocode(
            latlng=locations_dict[location]["place_id"])[0].get(
                "formatted_address")


def computeTime(locations_dict: dict, origin: str, mode: str) -> None:
    """
    Given a dictionary of all location, the starting address, and mode of transportation compute the time it takes to get to each location and add to dict.
    :param locations_dict: A dictionary with all the locations nearby
    :type locations_dict: dict
    :param origin: The address of the starting location
    :type origin: str
    :param mode: The type of transportation
    :type mode: str
    :return: None
    :rtype: None
    """
    # Make a list of Matrix for each type of transportation - distance_matrix()
    for location in locations_dict:
        locations_dict[location]["travel_time"] = gomaps.distance_matrix(
            origins=origin,
            destinations=locations_dict[location].get("address"),
            mode=mode)["rows"][0]["elements"][0].get("duration",
                                                     {}).get("text", {})


def removeFarLocations(locations_dict):
    """
    Given a dictionary of all location remove any location that is more then 20 min away
    :param locations_dict: A dictionary with all the locations nearby
    :type locations_dict: dict
    :return: None
    :rtype: None
    """
    #Remove locations that were found further than 20 minutes from your specified location -
    for location in list(locations_dict.keys()):
        if "hours" in locations_dict[location][
                "travel_time"] or "hour" in locations_dict[location][
                    "travel_time"]:
            del locations_dict[location]
    for location in list(locations_dict.keys()):
        num = locations_dict[location]["travel_time"]
        if len(num) == 0 or int(num.split()[0]) > 20:
            del locations_dict[location]

if __name__ == '__main__':
    # Get the starting location from the user
    origin_location = collectInfo()
    # Get the type of transportation the user wants to use
    selection = collectTransportation()
    # Create the dictionary of all the location
    locations_dict = serechForPlaces(getGeoCode(origin_location), RADIUS[0])
    # Add all the location address to data dict
    addLocationAddressData(locations_dict)
    # Compute the travel time for all location in dict
    computeTime(locations_dict, origin_location, MODE_OF_TRANS[selection])
    # Remove locations that take longer then 20 min
    removeFarLocations(locations_dict)
    # Display those locations
    displayPlaces(locations_dict)