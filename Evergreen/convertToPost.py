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

    StatusMapEvergreen = {
        "Gate out empty": "OA",
        "Gate in empty": "I",
        "Vessel departed": "VD",
        "Vessel arrived": "VA",
        "Loaded": "AE",
        "loaded on vessel": "AE",
        "Discharged": "UV",
        "Received": "CO",
        "Full import ": "CO",
        "Empty container received": "RD"
    }

def EvergreenCodeToName(code):
    if(code == "AE"):
        return "Loaded on Vessel"
    elif(code == "VD"):
        return "Vessel Departure"
    elif(code == "VA"):
        return "Vessel Arrival"
    elif(code == "UV"):
        return "Unloaded From Vessel"
    elif(code == "OA"):
        return "OUTGATE"
    elif(code == "I"):
        return "INGATE"
    elif(code == "CO"):
        return "Cargo Received"
    elif(code == "RD"):
        return "Return Container"
    return None

def EvergreenEventTranslate(event):
    for key, value in baseInfo.StatusMapEvergreen.items():
        if(event.find(key) != -1):
            return value, EvergreenCodeToName(value)
    return (None, None)
    


def EvergreenPost(container, path):
    if(os.path.isfile(path+"ContainerInformation\\"+container+".json")):
        with open(path+"ContainerInformation\\"+container+".json") as containerInfo:
            data = json.load(containerInfo)
            postJson = copy.deepcopy(baseInfo.shipmentEventBase)
            postJson["unitId"] = container
            postJson["location"] = data.get("Location")
            postJson["unitSize"] = data.get("Size/Type").split("'")[0]
            postJson["city"] = data.get("Location").split(" ")[0]
            postJson["eventTime"] = datetime.datetime.strptime(data.get("Date").title(), '%b-%d-%Y').strftime('%m-%d-%Y %H:%M:%S')
            try:
                print(data.get("Vessel Voyage").rsplit(' ', 1)[0])
                postJson["vessel"] = data.get("Vessel Voyage").rsplit(' ', 1)[0]
                postJson["voyageNumber"] = data.get("Vessel Voyage").rsplit(' ', 1)[1]
            except:
                return
            postJson["workOrderNumber"] = data.get("WONumber")
            postJson["billOfLadingNumber"] = data.get("BOLNumber")
            postJson["eventCode"], postJson["eventName"] = EvergreenEventTranslate(data.get("Container Moves"))
            postJson["resolvedEventSource"] = "Evergreen RPA"
            postJson["codeType"] = "UNLOCODE"
            postJson["reportSource"] = "OceanEvent"
            print(json.dumps(postJson))
            if(postJson["eventCode"] == None):
                return
            headers = {'content-type':'application/json'}
            r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
            print(r)
    return

def testMain(container):
    path=""
    for x in os.getcwd().split("\\"):
        path+=x+"\\\\"
    EvergreenPost(container, path)

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    for container in containerList:
        EvergreenPost(container, path)

if __name__ == "__main__":
    #testMain(sys.argv[1])
    main(sys.argv[1], sys.argv[2])
