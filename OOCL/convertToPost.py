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

    StatusMapOOCL = {
        "Arrived": "A",
        "Highway Arrival": "A",
        "Vessel Arrived": "VA",
        "Vessel Departed": "VD",
        "Loaded": "AE",
        "Discharged": "UV",
        "Carrier Released": "CR",
        "Container Received": "CO",
        "Picked Up for Delivery": "X3",
        "Container Returned": "RD",
        "Container Deramped": "UR",
        "Ramped": "AL",
        "Released": "CA"
    }

def OOCLCodeToName(code):
    if(code == "A"):
        return "ARRIVED"
    elif(code == "VA"):
        return "Vessel Arrival"
    elif(code == "VD"):
        return "Vessel Departure"
    elif(code == "AE"):
        return "Loaded on Vessel"
    elif(code == "UV"):
        return "Unloaded From Vessel"
    elif(code == "CR"):
        return "Carrier Release"
    elif(code == "CO"):
        return "Cargo Received"
    elif(code == "X3"):
        return "Arrived for Pickup"
    elif(code == "RD"):
        return "Return Container"
    elif(code == "UR"):
        return "UNLOADED_FROM_RAIL"
    elif(code == "AL"):
        return "LOADED_ON_RAIL"
    elif(code == "CA"):
        return "Cargo Available"
    return None

def OOCLEventTranslate(event):
    for key, value in baseInfo.StatusMapOOCL.items():
        if(event.find(key) != -1):
            return value, OOCLCodeToName(value)
    return (None, None)
    


def OOCLPost(container, path):
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
                postJson["eventTime"] = datetime.datetime.strptime(row[4].rsplit(" ", 1)[0], '%d %b %Y, %H:%M').strftime('%m-%d-%Y %H:%M:%S')
                postJson["vessel"] = row[7]
                postJson["voyageNumber"] = row[8]
                postJson["workOrderNumber"] = row[9]
                postJson["billOfLadingNumber"] = row[10]
                postJson["eventCode"], postJson["eventName"] = OOCLEventTranslate(row[0])
                if(postJson["eventCode"] == "AE" and row[3] == "Railway"):
                    postJson["eventCode"], postJson["EventName"] = ("AL","LOADED_ON_RAILWAY")
                postJson["resolvedEventSource"] = "OOCL RPA"
                postJson["codeType"] = "UNLOCODE"
                postJson["reportSource"] = "OceanEvent"
                print(json.dumps(postJson))
                if(postJson["eventCode"] == None):
                    continue
                headers = {'content-type':'application/json'}
                r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
                print(r)
    return

def testMain(container):
    path=""
    for x in os.getcwd().split("\\"):
        path+=x+"\\\\"
    OOCLPost(container, path)

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    for container in containerList:
        OOCLPost(container, path)

if __name__ == "__main__":
    #testMain(sys.argv[1])
    main(sys.argv[1], sys.argv[2])
