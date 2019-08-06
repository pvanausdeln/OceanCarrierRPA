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

    StatusMapMaersk = {
        "Gate out empty": "OA",
        "Gate in empty": "I",
        "Vessel departed": "VD",
        "Vessel arrived": "VA",
        "Loaded": "AE",
        "Discharged": "UV"
    }

def MaerskEventTranslate(event):
    if(event.find("Gate in") != -1):
        return ("Ingate Load", "I")
    elif(event.find("Load on") != -1):
        return ("Loaded on Vessel", "AE")
    elif(event.find("Discharge") != -1):
        return ("Unloaded from Vessel", "UV")
    elif(event.find("Gate out Empty") != -1):
        return ("Empty Equipment Dispatched", "EE")
    elif(event.find("On rail") != -1):
        return ("LOADED_ON_RAIL", "AL")
    elif(event.find("Off rail") != -1):
        return ("UNLOADED_FROM_RAIL", "UR")
    elif(event.find("Gate out Load") != -1):
        return ("Outgate Load", "OL")
    return (None, None)
    


def MaerskPost(container, path):
    if(os.path.isfile(path+"ContainerInformation\\"+container+".csv")):
        with open(path+"ContainerInformation\\"+container+".csv") as containerInfo:
            reader = csv.reader(containerInfo)
            next(reader) # skip first row
            for row in reader:
                postJson = copy.deepcopy(baseInfo.shipmentEventBase)
                postJson["unitId"] = container
                postJson["location"] = row[0]
                try:
                    postJson["eventTime"] = datetime.datetime.strptime(row[1].replace('\n', ' '), '%d %b %Y %H:%M').strftime('%m-%d-%Y %H:%M')+":00"
                except:
                    continue
                postJson["vessel"] = row[4]
                postJson["voyageNumber"] = row[5]
                postJson["eventName"], postJson["eventCode"] = MaerskEventTranslate(row[2])
                postJson["resolvedEventSource"] = "Maersk RPA"
                postJson["codeType"] = "UNLOCODE"
                postJson["reportSource"] = "OceanEvent"
                print(json.dumps(postJson))
                if(postJson["eventCode"] == None):
                    continue
                headers = {'content-type':'application/json'}
                r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
                print(r)
    return

def testMain(container): #test main
    path=""
    for x in os.getcwd().split("\\"):
        path+=x+"\\\\"
    MaerskPost(container, path)

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    for container in containerList:
        MaerskPost(container, path)

if __name__ == "__main__":
    testMain(sys.argv[1])
    #main(sys.argv[1], sys.argv[2])
