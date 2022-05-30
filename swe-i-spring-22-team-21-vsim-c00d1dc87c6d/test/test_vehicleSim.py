# Vehicle simulator unit test

import sys
import unittest

from classes.vsim import SimVehicle

sys.path.append("..")


class TestVehicle(unittest.TestCase):
    def setUp(self):
        self.vehicle = SimVehicle("abcd1234")


class TestInit(TestVehicle):
    def test_vehicleStatus(self):
        self.assertEqual(self.vehicle.vehicleStatus, "normal")

    def test_vehicle_ID(self):
        self.assertEqual(self.vehicle.vehicleID, "abcd1234")

    def test_vehicle_mileage(self):
        self.assertEqual(self.vehicle.vehicleMileage, 100)

    def test_gps_coords(self):
        self.assertEqual(self.vehicle.gpsCoords, [0.0, 0.0])

    def test_vehicle_charge(self):
        self.assertEqual(self.vehicle.vehicleCharge, 100)

    def test_status_default(self):
        self.assertEqual(self.vehicle.vehicleStatus, "normal")

    def test_route(self):
        self.assertEqual(self.vehicle.route, None)

    def test_route_status(self):
        self.assertEqual(self.vehicle.dispatchStatus, "none")

    def test_dispatch_ID(self):
        self.assertEqual(self.vehicle.dispatchID, "")

    def test_heartbeat_time(self):
        self.assertEqual(self.vehicle.time, 5)

    def test_default_fleet(self):
        self.assertEqual(self.vehicle.fleet, "")

    def test_setGPS_setGPS(self):
        newCoords = [-123.45, 67.890]
        self.vehicle.setGPSLocation(newCoords)
        self.assertEqual(self.vehicle.getGPSLocation(), newCoords)

    def test_heartbeat_setTime(self):
        newTime = 7
        self.vehicle.setHeartbeatTime(newTime)
        self.assertEqual(self.vehicle.getHeartbeatTime(), newTime)

    def test_route_setGet(self):
        newRoute = [[12.34, 56.78], [32.10, 98.76], [10.20, 30.40]]
        self.vehicle.setRoute(newRoute)
        self.assertEqual(self.vehicle.getRoute(), newRoute)

    def test_manualPosition(self):
        print("enter 123.45 for both locations")
        self.vehicle.manualGPS()
        newPosition = [123.45, 123.45]
        self.assertEqual(self.vehicle.getGPSLocation(), newPosition)

    def test_setRouteFile(self):
        file = open("package.json") # open included route file
        routeFile = file.read()
        file.close()
        self.vehicle.setRouteFile(routeFile)
        self.assertEqual(self.vehicle.routeFile, routeFile)

    def test_extractRoute(self):
        file = open("package.json") # open included route file
        self.vehicle.setRouteFile(file.read())
        self.vehicle.extractRoute()
        file.close()
        newRoute = [[-97.739046, 30.26702], [-97.744126, 30.26844], [-97.74378, 30.269365], [-97.743577, 30.269308], [-97.743577, 30.269308], [-97.743134, 30.269184], [-97.743498, 30.268265], [-97.746282, 30.269042], [-97.747681, 30.265288], [-97.747049, 30.265112]]
        self.assertEqual(self.vehicle.route, newRoute)

    def test_printVehicle(self):
        self.vehicle.printVehicle()

    def test_updateVehicle(self):
        newFile = open("dispatchResponse.json")
        self.vehicle.updateVehicleGetCall(newFile.read())
        newFile.close()
        newFleet = "j3n8NAyB"
        newDispatchStatus = "in-progress"
        newDispatchID = "6uIdZ76p"
        newDispatchRoute = [[-97.743577, 30.269308], [-97.734686, 30.266827], [-97.73508, 30.265756], [-97.741481, 30.233463], [-97.747739, 30.223529], [-97.754122, 30.226749], [-97.753542, 30.227846], [-97.754225, 30.228129], [-97.754225, 30.228129], [-97.757015, 30.229286], [-97.75749, 30.228367], [-97.760242, 30.229656], [-97.763418, 30.223763], [-97.788074, 30.230338], [-97.79681, 30.216393], [-97.797212, 30.216419]]
        self.assertEqual(self.vehicle.fleet, newFleet)
        self.assertEqual(self.vehicle.dispatchID, newDispatchID)
        self.assertEqual(self.vehicle.dispatchStatus, newDispatchStatus)
        self.assertEqual(self.vehicle.route, newDispatchRoute)

    def test_heartbeat(self):
        newFile = open("dispatchResponse.json")
        self.vehicle.updateVehicleGetCall(newFile.read())
        newFile.close()
        self.vehicle.heartbeat()

if __name__ == '_main_':
    unittest.main()
