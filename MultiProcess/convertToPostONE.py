import os
import sys
import json
import copy
import requests
import datetime
import glob
import csv
import string

class baseInfo:
    postURL = "https://test-apps.blumesolutions.com/shipmentservice-api/v1/bv/shipmentevents"

    shipmentEventBase = {
    "associatedAssetSize": None,
    "associatedUnitId": None,
    "billOfLadingNumber": None,
    "bookingNumber": None,
    "bookingOffice": None,
    "carrierCode": None,
    "carrierName": None,
    "city": None,
    "codeType": None,
    "consigneeName": None,
    "containerBookingNumber": None,
    "country": None,
    "createdBy": None,
    "customerOrderReferenceNumber": None,
    "destinationCity": None,
    "destinationSPLC": None,
    "destinationState": None,
    "eventCode": None,
    "eventName": None,
    "eventTime": None,
    "houseBill": None,
    "importReferenceNumber": None,
    "latitude": 0,
    "location": None,
    "longitude": 0,
    "masterBill": None,
    "notes": None,
    "onHandNumber": None,
    "originSPLC": None,
    "originatorCode": None,
    "originatorId": 0,
    "originatorName": None,
    "postalCode": None,
    "purchaseOrderReferenceNumber": None,
    "railBillingNumber": None,
    "reasonCode": None,
    "reasonName": None,
    "receiverCode": None,
    "receiverName": None,
    "reportSource": None,
    "reportedBy": None,
    "resolvedEventId": 0,
    "resolvedEventOriginalId": 0,
    "resolvedEventSource": None,
    "resolvedEventStatus": None,
    "sealNumber": None,
    "shipmentReferenceNumber": None,
    "signedBy": None,
    "state": None,
    "stopType": None,
    "terminalCode": None,
    "terminalFunction": None,
    "unitId": None,
    "unitSize": 0,
    "unitState": None,
    "unitTypeCode": None,
    "vessel": None,
    "voyageNumber": None,
    "workOrderNumber": None
    }

    StatusMapONE = {
        "Gate In to Outbound": "I",
        " at Port of Loading": "AE",
        "Departure from Port of Loading": "VD",
        "Arrival at Port of Discharging": "VA",
        " at Port of Discharging": "UV",
        "Gate Out from Inbound": "OA",
        "Rail Departure": "RL",
        "Rail Arrival": "AR",
        "Loaded on rail": "AL",
        "Unloaded from rail": "UR",
        "Empty Container Returned": "RD",
        "Empty Container Release": "EE",
		"Loaded at Port of Transshipment":"LPOT",
		"Unloaded at Port of Transshipment":"UNPOT",
		"Arrival at Port of Transshipment":"APOT",
		"Departure from Port of Transshipment":"DPOT",
		"T/S Berthing":"TB",
		"POD Berthing":"PODB",
		"Feeder Arrival":"FA",
		"Feeder Departure":"FD",
		"Feeder Loading":"FL",
		"Feeder Unloading":"FUL",
		"Water POL Unloading Destination":"WD",
        "Truck Terminal Departure": "TTD",
        "Truck Terminal Arrival": "TTA"
		
    }

def ONECodeToName(code):
    if(code == "AE"):
        return "Loaded on Vessel"
    elif(code == "I"):
        return "INGATE"
    elif(code == "VD"):
        return "Vessel Departure"
    elif(code == "VA"):
        return "Vessel Arrival"
    elif(code == "UV"):
        return "Unloaded From Vessel"
    elif(code == "OA"):
        return "OUTGATE"
    elif(code == "RL"):
        return "Rail Departure"
    elif(code == "AR"):
        return "Rail Arrival"
    elif(code == "AL"):
        return "Loaded on Rail"
    elif(code == "UR"):
        return "Unloaded from Rail"
    elif(code == "RD"):
        return "Return Container"
    elif(code == "EE"):
        return "Empty Equipment Dispatched"
    elif(code == "LPOT"):
        return "Loaded at Port of Transshipment"
    elif(code == "UNPOT"):
        return "Unloaded at Port of Transshipment"
    elif(code == "APOT"):
        return "Arrival at Port of Transshipment"
    elif(code == "DPOT"):
        return "Departure from Port of Transshipment"
    elif(code == "TB"):
        return "T/S Berthing"
    elif(code == "PODB"):
        return "POD Berthing"
    elif(code == "FA"):
        return "Feeder Arrival"
    elif(code == "FD"):
        return "Feeder Departure"
    elif(code == "FL"):
        return "Feeder Loading"
    elif(code == "FUL"):
        return "Feeder Unloading"
    elif(code == "WD"):
        return "Water POL Unloading Destination"
    elif(code == "TTD"):
        return "Truck Terminal Departure"
    elif(code == "TTA"):
        return "Truck Terminal Arrival"
    return None

def ONEEventTranslate(event):
    for key, value in baseInfo.StatusMapONE.items():
        if(event.find(key) != -1):
            return value, ONECodeToName(value)
    return (None, None)



def ONEPost(container, path):
    if(os.path.isfile(path+"ContainerInformation\\"+container+".csv")):
        with open(path+"ContainerInformation\\"+container+".csv") as containerInfo:
            reader = csv.reader(containerInfo)
            next(reader)
            for row in reader:
                postJson = copy.deepcopy(baseInfo.shipmentEventBase)
                postJson["unitId"] = container
                postJson["location"] = row[2].split("\n")[0]
                postJson["city"] = postJson["location"].split(",")[0]
                postJson["country"] = postJson["location"].split(",")[-1]
                if(row[3].strip() == ""):
                    continue
                postJson["eventTime"] = datetime.datetime.strptime(" ".join(row[3].strip().split(" ")[1:]), '%Y-%m-%d %H:%M').strftime('%m-%d-%Y %H:%M:%S')
                postJson["vessel"] = row[4]
                postJson["voyageNumber"] = row[5]
                postJson["eventCode"], postJson["eventName"] = ONEEventTranslate(row[1])
                postJson["resolvedEventSource"] = "ONE RPA"
                postJson["codeType"] = "UNLOCODE"
                postJson["reportSource"] = "OceanEvent"
                print(json.dumps(postJson))
                if(postJson["eventCode"] == None):
                    continue
                headers = {'content-type':'application/json'}
                r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
                print(r)
    return

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    containerList = list(set(containerList))
    for container in containerList:
        ONEPost(container, path)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
