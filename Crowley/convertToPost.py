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

    StatusMapCrowley = {
        "Gate out empty": "OA",
        "Gate in empty": "I",
        "Vessel departed": "VD",
        "Vessel arrived": "VA",
        "Loaded": "AE",
        "Discharged": "UV"
    }

def CrowleyEventTranslate(event):
    if(event.find("Departed Empty") != -1 or event.find("Equipment Assigned") != -1):
        return ("Empty Equipment Dispatched", "EE")
    elif(event.find("Received ") != -1):
        return ("Cargo Received", "CO")
    elif(event.find("Loaded onto Vessel") != -1):
        return ("Loaded on Vessel", "AE")
    elif(event.find("Vessel has Sailed") != -1):
        return ("Vessel Departure", "VD")
    elif(event.find("Available for pickup") != -1):
        return ("Cargo Available", "CA")
    elif(event.find("Dispatched") != -1):
        return ("Outgate Load", "OL")
    elif(event.find("Confirmed ") != -1): # placeholder
        return (None, None)
    return (None, None)
    


def CrowleyPost(step):
    with open(step) as jsonData:
        data = json.load(jsonData)
    postJson = copy.deepcopy(baseInfo.shipmentEventBase)
    postJson["unitId"] = data.get("ContainerID")
    postJson["location"] = data.get("Event").split("at")[-1].strip()
    postJson["city"] = postJson["location"].split(",")[0]
    postJson["eventTime"] = datetime.datetime.strptime(data.get("Datetime"), '%Y-%m-%d %H:%M').strftime('%m-%d-%Y %H:%M:%S')

    postJson["vessel"] = "PARADERO"#data.get("Vessel")
    postJson["voyageNumber"] = "023N"#data.get("Voyage")
    postJson["workOrderNumber"] = data.get("WONumber")
    postJson["billOfLadingNumber"] = data.get("BOLNumber")

    postJson["eventName"], postJson["eventCode"] = CrowleyEventTranslate(data.get("Event"))
    postJson["resolvedEventSource"] = "Crowley RPA"
    postJson["codeType"] = "UNLOCODE"
    postJson["reportSource"] = "OceanEvent"
    print(json.dumps(postJson))
    if(postJson["eventCode"] == None):
        return
    headers = {'content-type':'application/json'}
    r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    print(r)
    return

def testMain(container): #test main
    fileList = glob.glob(os.getcwd() + "\\ContainerInformation\\"+container+"Step*.json", recursive = True) #get all the json steps
    if (not fileList):
        return
    fileList = [f for f in fileList if container in f] #set of steps for this number
    fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
    for step in fileList:
        CrowleyPost(step)

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    for container in containerList:
        fileList = glob.glob(r""+path+"ContainerInformation\\"+container+'Step*.json', recursive = True) #get all the json steps
        if (not fileList):
            continue
        fileList = [f for f in fileList if container in f] #set of steps for this number
        fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
        for step in fileList:
            CrowleyPost(step)

if __name__ == "__main__":
    #testMain(sys.argv[1])
    main(sys.argv[1], sys.argv[2])
