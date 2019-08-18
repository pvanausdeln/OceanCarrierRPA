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

    StatusMapHyundai = {
        "Gate out empty": "OA",
        "Gate in empty": "I",
        "Vessel Departed": "VD",
        "Vessel Arrived": "VA",
        "Loaded": "AE",
        "Discharged": "UV"
    }

def HyundaiCodeToName(code):
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
    return None

def HyundaiEventTranslate(event):
    for key, value in baseInfo.StatusMapHyundai.items():
        if(event.find(key) != -1):
            return value, HyundaiCodeToName(value)
    return (None, None)



def HyundaiPost(step):
    # if(os.path.isfile(path+"ContainerInformation\\"+container+".csv")):
    #     with open(path+"ContainerInformation\\"+container+".csv") as containerInfo:
    #         reader = csv.reader(containerInfo)
    #         next(reader) # skip first row
    #         for row in reader:
    with open(step) as jsonData:
        data = json.load(jsonData)
    postJson = copy.deepcopy(baseInfo.shipmentEventBase)
    postJson["unitId"] = data["ContainerID"]
    postJson["location"] = data["Location"].split("\n")[0]
    postJson["city"] = postJson["location"].split(",")[0]
    postJson["eventTime"] = datetime.datetime.strptime(data["Date"]+" "+data["Time"].split(" ")[0], '%d-%b-%Y %H:%M').strftime('%m-%d-%Y %H:%M:%S')
    # postJson["vessel"] = row[11]
    # postJson["voyageNumber"] = row[12]
    # postJson["workOrderNumber"] = row[14]
    # postJson["billOfLadingNumber"] = row[13]
    postJson["eventCode"], postJson["eventName"] = HyundaiEventTranslate(data["Status Description"])
    postJson["resolvedEventSource"] = "Hyundai RPA"
    postJson["codeType"] = "UNLOCODE"
    postJson["reportSource"] = "OceanEvent"
    print(json.dumps(postJson))
    if(postJson["eventCode"] == None):
        return
    headers = {'content-type':'application/json'}
    r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
    print(r)
    return

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    for container in containerList:
        fileList= glob.glob(r""+path+"ContainerInformation\\"+container+"Step*.json", recursive= True)
        if (not fileList):
            continue
        fileList = [f for f in fileList if container in f] #set of steps for this number
        fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
        for step in fileList:
            HyundaiPost(step)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
