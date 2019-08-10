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

    StatusMapCOSCO = {
        "Empty Equipment Despatched": "EE",
        "Cargo Received": "CO",
        "Gate-in at First POL": "I",
        "Loaded at First POL": "AE",
        "Discharge at Last POL": "UV",
        "Gate-out from Last POD": "AL",
        "First Loaded on Rail under I/B": "RL",
        "Gate-in at Final Hub": "I",
        "Last Arrival under I/B": "AR",
        "Rail Arrival at Final Hub": "DA",
        "De-ramp at Final Hub": "D",
        "Last De-ramp under I/B": "D1",
        "Gate-out from Final Hub": "OA",
        "Emopty Equipment Returned": "RD",
        "Discharged at T/S POD": "UV",
        "Loaded at T/S POL": "AE",
        "Transfer": "LOL",
        "Gate-out from First Full Facility": "LMAO"
    }

def COSCOCodeToName(code):
    if(code == "EE"):
        return "Empty Equipment Dispatched"
    elif(code == "CO"):
        return "Cargo Received"
    elif(code == "OL"):
        return "Outgate Load"
    elif(code == "AL"):
        return "Loaded on Rail"
    elif(code == "RL"):
        return "Rail Departure"
    elif(code == "AR"):
        return "Rail Arrival"
    elif(code == "DA"):
        return "Destination Arrival"
    elif(code == "D"):
        return "Unloaded at Destination"
    elif(code == "D1"):
        return "Unloading Complete"
    elif(code == "RD"):
        return "Return Container"
    elif(code == "AE"):
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

def COSCOEventTranslate(event):
    for key, value in baseInfo.StatusMapCOSCO.items():
        if(event.find(key) != -1):
            return value, COSCOCodeToName(value)
    return (None, None)
    


def COSCOPost(container, path):
    if(os.path.isfile(path+"ContainerInformation\\"+container+".csv")):
        with open(path+"ContainerInformation\\"+container+".csv") as containerInfo:
            reader = csv.reader(containerInfo)
            next(reader) # skip first row
            for row in reader:
                postJson = copy.deepcopy(baseInfo.shipmentEventBase)
                postJson["unitId"] = container
                postJson["location"] = row[1].split("\n")[0]
                postJson["city"] = postJson["location"].split(",")[0]
                if(row[2].strip() == "" or row[3].strip() == ""):
                    continue
                postJson["eventTime"] = datetime.datetime.strptime(row[2]+" "+row[3], '%Y-%m-%d %H:%M').strftime('%m-%d-%Y %H:%M:%S')
                postJson["vessel"] = row[11]
                postJson["voyageNumber"] = row[12]
                postJson["workOrderNumber"] = row[14]
                postJson["billOfLadingNumber"] = row[13]
                postJson["eventCode"], postJson["eventName"] = COSCOEventTranslate(row[0])
                postJson["resolvedEventSource"] = "COSCO RPA"
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
        COSCOPost(container, path)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
