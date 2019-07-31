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

def CMACGMEventTranslate(event):
    if(event.find("Loaded") != -1 or event.find("Transshipment Loaded") != -1):
        return ("Loaded on Vessel", "AE")
    elif(event.find("Carrier Release") != -1):
        return ("Carrier Release", "CR")
    elif(event.find("Customs Release") != -1):
        return ("Customs Release", "CT")
    elif(event.find("Transshipment Discharged") != -1):
        return ("Unloaded from Vessel", "UV")
    elif(event.find("Gate Out Full") != -1):
        return ("Outgate Load", "OL")
    elif(event.find("Empty to shipper") != -1):
        return ("Empty Equipment Dispatched", "EE")
    elif(event.find("Empty in Container Yard") != -1):
        return ("Return Container", "RD")
    elif(event.find("Gate In Full") != -1):
        return ("Ingate Load", "I")
    elif(event.find("Loaded on Rail") != -1):
        return ("LOADED_ON_RAIL", "AL")
    elif(event.find("Rail departed Origin") != -1):
        return ("RAIL_DEPARTURE", "RL")
    elif(event.find("Arrived at rail ramp") != -1):
        return ("RAIL_ARRIVAL", "AR")
    elif(event.find("Unloaded from Rail") != -1):
        return ("UNLOADED_FROM_RAIL", "UR")
    return (None, None)



def CMACGMPost(container, path):
    if(os.path.isfile(path+"ContainerInformation\\"+container+".csv")):
        with open(path+"ContainerInformation\\"+container+".csv") as containerInfo:
            reader = csv.reader(containerInfo)
            next(reader)

            for row in reader:
                if(row[0].find("Provisional moves not found, please feel free to use Contact Support link for more information")!= -1):
                    continue
                postJson = copy.deepcopy(baseInfo.shipmentEventBase)
                postJson["unitId"] = container
                postJson["location"] = row[3]
                postJson["city"] = postJson["location"].split(",")[0]
                postJson["eventTime"] = datetime.datetime.strptime(row[0], '%a %d %b %Y %H:%M').strftime('%m-%d-%Y %H:%M:%S')
                postJson["vessel"] = str(row[4])
                postJson["voyageNumber"] = str(row[5])
                postJson["workOrderNumber"] = row[6]
                postJson["billOfLadingNumber"] = row[7]
                postJson["unitType"] = row[8]
                postJson["eventName"], postJson["eventCode"] = CMACGMEventTranslate(row[2])
                postJson["resolvedEventSource"] = "CMACGM RPA"
                postJson["codeType"] = "UNLOCODE"
                postJson["reportSource"] = "OceanEvent"
                print(json.dumps(postJson))
                if(postJson["eventCode"] == None):
                    continue
                headers = {'content-type':'application/json'}
                r = requests.post(baseInfo.postURL, data = json.dumps(postJson), headers = headers, verify = False)
                # print(r)

    return

def testMain(container): #test main
    fileList = glob.glob(os.getcwd() + "\\ContainerInformation\\"+container+".csv", recursive = True) #get all the json steps
    if (not fileList):
        return
    fileList = [f for f in fileList if container in f] #set of steps for this number
    fileList.sort(key=os.path.getmtime) #order steps correctly (by file edit time)
    for step in fileList:
        CMACGMPost(step)

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    for container in containerList:
        CMACGMPost(container, path)

if __name__ == "__main__":
    #testMain(sys.argv[1])
    main(sys.argv[1], sys.argv[2])
