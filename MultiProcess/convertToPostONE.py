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
        "Gate In to Outbound Terminal": "I",
        " at Port of Loading\n": "AE",
        "Departure from Port of Loading\n": "VD",
        "Arrival at Port of Discharging\n": "VA",
        " at Port of Discharging\n": "UV",
        "Gate Out from Inbound Terminal": "OA"
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
                postJson["workOrderNumber"] = row[6]
                postJson["billOfLadingNumber"] = row[7]
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
    for container in containerList:
        hi=ONEPost(container, path)
    return hi

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
