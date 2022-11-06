import os
import requests

API_key = (os.getenv("API_key"))


def calc_distance(origin, destination, mode):
    base_url ="https://maps.googleapis.com/maps/api/distancematrix/json?&units=imperial&"
    response = requests.get(base_url + "origins=" + origin + "&destinations=" + destination + "&mode=" + mode + "&key=" + API_key)
    time = response.json()["rows"][0]["elements"][0]["duration"]["text"]
    seconds = response.json()["rows"][0]["elements"][0]["duration"]["value"]
    print("It takes " + time + " to get there")
    print(response.text)



#origin = input("Please enter your origin: ")
#destination = input("Please enter your destination: ")
#mode = input("Enter your mode of transportation: ")


def find_place():
  
    
  base_url = ("https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=mongolian&inputtype=textquery&locationbias=circle%3A2000%4047.6918452%2C-122.2226413&fields=formatted_address%2Cname%2Crating%2Copening_hours%2Cgeometry&key="+API_key)

  headers = {}
  payload = {}

  response = requests.request("GET", base_url, headers=headers, data=payload)

  print(response.text)


#when the api key is hidden, the API call does not work
#change functionality to ask the user to pass in their location and then show what is in 20 minutes proximity
#origin and destination are the required parameters
#how to modify the response to the conditions we want
# use of a loop 


# Food, Medical, Government, Green space, Transportation
# list of restaurants in the area
# if the user's destination is == to any elements of the list
# return the duration it takes
# easier to find out if there are restaurants within 20 minutes
def main():
  find_place()

if __name__ == '__main__':
    main()