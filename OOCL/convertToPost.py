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
    postURL = "https://demo-apps.blumesolutions.com/shipmentservice-api/v1/bv/shipmentevents"

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
        "Vessel Arrived": "VA",
        "Vessel Departed": "VD",
        "Loaded": "AE",
        "Discharged": "UV",
        "Carrier Released": "CR"
    }

def OOCLCodeToName(code):
    if(code == "VA"):
        return "Vessel Arrival"
    elif(code == "VD"):
        return "Vessel Departure"
    elif(code == "AE"):
        return "Loaded on Vessel"
    elif(code == "UV"):
        return "Unloaded From Vessel"
    elif(code == "CR"):
        return "Carrier Release"
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
                postJson["eventTime"] = datetime.datetime.strptime(row[3], '%Y-%m-%d %H:%M').strftime('%m-%d-%Y %H:%M:%S')
                postJson["vessel"] = row[4]
                postJson["voyageNumber"] = row[5]
                postJson["workOrderNumber"] = row[6]
                postJson["billOfLadingNumber"] = row[7]
                postJson["eventCode"], postJson["eventName"] = OOCLEventTranslate(row[1])
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

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    for container in containerList:
        OOCLPost(container, path)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
