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
    postURL = "https://demo-api.iasdispatchmanager.com:8502/v1/bv/shipmentevents"

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

    StatusMapUSLines  = {
        "Empty to shipper": ("CD", "Received at Origin"),
        "Loaded on board": ("AE", "Loaded on Vessel"),
        "Full Load on rail for import": ("AL", "Loaded on Rail"),
        "Discharged in transhipment": ("UE", "Unloaded from Vessel"),
        "Train arrival for import": ("AR", "Rail Arrival at Destination Intermodal Ramp"),
        "Import unload full from rail": ("UR", "Unloaded from a Rail Car"),
        "Container to cosignee": ("X1", "Arrived at Delivery Location")
    }


def USLinesEventTranslate(event):
    for key, value in baseInfo.StatusMapUSLines.items():
        if(event.find(key) != -1):
            return value
    return (None, None)
    


def USLinesPost(container, path):
    if(os.path.isfile(path+"ContainerInformation\\"+container+".csv")):
        with open(path+"ContainerInformation\\"+container+".csv") as containerInfo:
            reader = csv.reader(containerInfo)
            next(reader)
            for row in reader:
                postJson = copy.deepcopy(baseInfo.shipmentEventBase)
                postJson["unitId"] = container
                postJson["location"] = row[3]
                postJson["city"] = postJson["location"].split(",")[0]
                postJson["eventTime"] = datetime.datetime.strptime(row[0], '%a %d %b %Y %H:%M').strftime('%m-%d-%Y %H:%M:%S')
                postJson["vessel"] = row[4]
                postJson["voyageNumber"] = row[5]
                postJson["workOrderNumber"] = row[6]
                postJson["billOfLadingNumber"] = row[7]
                postJson["unitType"] = row[8]
                postJson["eventCode"], postJson["eventName"] = USLinesEventTranslate(row[2])
                postJson["resolvedEventSource"] = "USLines RPA"
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
        USLinesPost(container, path)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
