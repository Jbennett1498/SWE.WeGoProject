# This is a vehicle simulator class.
# The goal of the heartbeat and vsim is to regularly send a PATCH API-request to our supply server sending the
# vehicles current GPS location
# as well as the job status, battery charge, mileage, vehicle#, vehicle status.

import json
from time import sleep
import requests


class SimVehicle:

    # constructor
    def __init__(self, vehicleIDNumber, defaultVehicleMileage=100, defaultVehicleCharge=100,
                 defaultVehicleStatus="normal", defaultRoute=None, defaultDispatchStatus="none", defaultDispatchID="",
                 defaultTime=5):
        self.vehicleID = vehicleIDNumber
        self.vehicleMileage = defaultVehicleMileage
        self.gpsCoords = [0.0, 0.0]
        self.vehicleCharge = defaultVehicleCharge
        self.vehicleStatus = defaultVehicleStatus
        self.route = defaultRoute
        self.dispatchStatus = defaultDispatchStatus
        self.dispatchID = defaultDispatchID
        self.time = defaultTime
        self.fleet = ""
        self.routeFile = None

    def setGPSLocation(self, gpsCoordinates):
        self.gpsCoords = gpsCoordinates

    def getGPSLocation(self):
        return self.gpsCoords

    def setHeartbeatTime(self, newTime):
        self.time = newTime

    def getHeartbeatTime(self):
        return self.time

    def setRoute(self, newRoute):
        self.route = newRoute

    def setRouteFile(self, jsonFile):
        self.routeFile = jsonFile

    def getRoute(self):
        return self.route

    def manualGPS(self):

        print("Enter Longitude:")
        rawInput = input()
        long = float(rawInput)
        print("Enter Latitude:")
        rawInput = input()
        lat = float(rawInput)

        # combine values in order that Mapbox expects longitude and latitude
        coordinates = [lat, long]

        # assign value
        self.setGPSLocation(coordinates)

        # send PATCH call to update vehicle's current location
        self.supplyPatchCall()

    # This function will send PATCH API Request to the Supply Server
    def heartbeat(self):
        # flag for running Heartbeat function
        runningHeartbeat = True
        routePosition = 0

        # Set current position to starting place of route, set dispatch status as "in-progress"
        self.gpsCoords = self.route[routePosition]
        self.dispatchStatus = "in-progress"

        # start loop
        while runningHeartbeat:
            # set timer
            sleep(self.time)

            if self.dispatchStatus == "in-progress":
                # id which route position we're at
                print("step " + str(routePosition + 1) + " of " + str(len(self.route)))

            # send get request
            # getResponse = self.supplyGetCall()

            # if not handling a route, check GET for updates
            if self.dispatchStatus != "in-progress":
                # self.updateVehicleGetCall(getResponse.json())  # Commented out while API is not active
                print("Update per GET call.")

            # send patch (heartbeat)
            self.supplyPatchCall()

            # display vehicle details
            self.printVehicle()

            # mimics depreciating vehicle charge and increasing mileage
            self.vehicleCharge -= 1
            self.vehicleMileage += 1
            if self.vehicleCharge < 0:
                print("Battery dead")
                runningHeartbeat = False

            # If actively on a job and not at the end of a route, iterate through location array and update location
            if routePosition < (len(self.route) - 1) and (self.dispatchStatus == "in-progress"):
                routePosition += 1
                self.gpsCoords = self.route[routePosition]

            # once at end of route, drop route, dispatch id and route file, and update dispatch status
            elif routePosition >= (len(self.route) - 1) and (self.dispatchStatus == "in-progress"):
                print("End of dispatch. Updating vehicle and sending current status to supply server")
                self.dispatchStatus = 'waiting'
                self.dispatchID = ""
                self.route = []
                self.routeFile = None
                routePosition = 0
                self.supplyPatchCall()
                # comment out if you want to keep the heartbeat going after reaching end of route
                runningHeartbeat = False
            else:
                print("Waiting on new dispatch orders")

    # This function will interpret the route object and get driving coordinates
    # This function is expecting a Mapbox route object with the 'Steps' option set to 'true' and
    # two legs, one for getting the vehicle to the customer,
    # and one for getting the customer to the destination.
    def extractRoute(self):
        if type(self.routeFile) is str:
            data = json.loads(self.routeFile)
            routes = data['routes']
            routeData = routes[0]  # routeData is a dict
            legs = routeData['legs']  # list
            leg1 = legs[0]  # dict
            leg2 = legs[1]  # dict
            leg1steps = leg1['steps']  # list
            leg2steps = leg2['steps']  # list
            route1 = list(map(lambda x: x['maneuver']['location'],
                              leg1steps))  # extract the location of each maneuver from the first leg
            route2 = list(map(lambda x: x['maneuver']['location'],
                              leg2steps))  # extract the location of each maneuver from the second leg
            finalRoute = route1 + route2  # combine into single array
            self.route = finalRoute

        elif type(self.routeFile is dict):
            data = self.routeFile
            routes = data['routes']
            routeData = routes[0]  # routeData is a dict
            legs = routeData['legs']  # list
            leg1 = legs[0]  # dict
            leg2 = legs[1]  # dict
            leg1steps = leg1['steps']  # list
            leg2steps = leg2['steps']  # list
            route1 = list(map(lambda x: x['maneuver']['location'],
                              leg1steps))  # extract the location of each maneuver from the first leg
            route2 = list(map(lambda x: x['maneuver']['location'],
                              leg2steps))  # extract the location of each maneuver from the second leg
            finalRoute = route1 + route2  # combine into single array
            self.route = finalRoute

        else:
            print("No route file established. Use 'setRouteFile' with a json file passed from Mapbox's directions API")

    def printVehicle(self):
        print("**********************************************")
        print("Vehicle id: " + self.vehicleID)
        print("Current coords: ")
        print(self.gpsCoords)
        print("Mileage: " + str(self.vehicleMileage))
        print("Charge: " + str(self.vehicleCharge))
        print("Vehicle Status: " + self.vehicleStatus)
        print("Dispatch Status: " + self.dispatchStatus)
        print("Dispatch ID: " + str(self.dispatchID))
        print("Route coordinates:")
        print(self.route)
        print("**********************************************")

    def supplyPatchCall(self):
        print("Sending PATCH call")
        url = "https://supply.team21.sweispring22.gq/v1/vehicles/" + str(self.vehicleID)

        # convert current gps to string
        currentLocation = str(self.gpsCoords[0]) + "," + str(self.gpsCoords[1])
        payload = json.dumps({
            "charge": self.vehicleCharge,
            "mileage": self.vehicleMileage,
            "service_status": self.vehicleStatus,
            "job_status": self.dispatchStatus,
            "dispatch": self.dispatchID,
            "position": currentLocation,
            "route": self.routeFile
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer <Bearer Token>'
        }

        # no return value because the Vehicle PATCH endpoint does not have a return object.
        # patchResponse = requests.request("PATCH", url, headers=headers, data=payload)

    def supplyGetCall(self):
        print("Sending GET call")
        url = "https://supply.team21.sweispring22.gq/v1/vehicles/" + str(self.vehicleID)

        payload = {}
        headers = {
            'Accept': 'application/json'
        }

        # response = requests.request("GET", url, headers=headers, data=payload)
        # print(response)
        # getCallData = json.loads(response.json())
        # return response

    # GET Vehicle call returns id (String), fleet (string), vin (string), make(string), model(string)
    # year(int), charge(int), mileage (int), service_status(new, check-engine, normal, totaled, passenger-dead),
    # job_status(in-progress, waiting, none), dispatch (string), position (string) and route(json obj)
    def updateVehicleGetCall(self, responseJSON):
        # Extract dictionary from JSON file passed
        responseDict = json.loads(responseJSON)

        # Now simply check certain variables to see if any statuses would change, and then update as needed
        if self.dispatchStatus != responseDict["job_status"]:
            self.dispatchStatus = responseDict["job_status"]

        if self.dispatchID != responseDict["dispatch"]:
            self.dispatchID = responseDict["dispatch"]

        if self.fleet != responseDict["fleet"]:
            self.fleet = responseDict["fleet"]

        if self.routeFile != responseDict["route"]:
            self.routeFile = responseDict["route"]
            self.extractRoute()
