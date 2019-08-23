import os
import sys
import json
import copy
import requests
import datetime
import glob
import csv
import string
import re
import kafka

class baseInfo:
    postURL = "https://apps.blumesolutions.com/shipmentservice-api/v1/bv/shipmentevents"

    shipmentEventBase = {
        "billOfLadingNumber": None,
        "bookingNumber": None,
        "carrierCode": None,
        "carrierName": None,
        "city": None,
        "codeType": None,
        "country": None,
        "estimatedEvent": False,
        "eventCode": None,
        "eventName": None,
        "eventTime": None,
        "estimatedEvent": False,
        "location": None,
        "reportSource": None,
        "resolvedEventSource": None,
        "shipmentReferenceNumber": None,
        "state": None,
        "terminalCode": None,
        "unitId": None,
        "unitSize": 0,
        "unitTypeCode": None,
        "vessel": None,
        "voyageNumber": None,
        "workOrderNumber": None
    }

def CMACGMEventTranslate(event):
    if(event.find("Loaded on board") != -1):
        return ("Loaded on Vessel", "AE")
    elif(event.find("Discharged in transhipment") != -1):
        return ("Unloaded from Vessel", "UV")
    elif(event.find("Ready to be loaded") != -1):
        return ("Prepared for Loading", "PRE")
    elif(event.find("Departure") != -1):
        return ("Vessel Departure", "VD")
    elif(event.find("Discharge") != -1):
        return ("Unloaded from Vessel", "UV")
    elif(event.find("Arrival final port") != -1):
        return ("Vessel Arrival", "VA")
    elif(event.find("Received for ") != -1):
        return ("Received", "R")
    elif(event.find("Empty in Container Yard") != -1):
        return ("Return Container", "RD")
    elif(event.find("Gate In Full") != -1):
        return ("Ingate Load", "I")
    elif(event.find("Full Load on rail") != -1 or event.find("Container on rail for import") != -1  or event.find("Container on rail for export") != -1):
        return ("Loaded on Rail", "AL")
    elif(event.find("Container in transit ") != -1):
        return ("In Transit", "IT")
    elif(event.find("Rail departed Origin") != -1):
        return ("RAIL_DEPARTURE", "RL")
    elif(event.find("Train arrival for export") != -1 or event.find("Train arrival for import") != -1):
        return ("Rail Arrival at Destination Intermodal Ramp", "AR")
    elif(event.find("Export unload full from rail") != -1 or event.find("Import unload full from rail") != -1):
        return ("Unloaded from a rail car", "UR")
    elif(event.find("Empty in depot") != -1):
        return ("Return Container", "RD")
    elif(event.find("Empty to shipper") != -1):
        return ("Empty Equipment Dispatched", "EE")
    return (None, None)



def CMACGMPost(container, path):

    if(os.path.isfile(path+"ContainerInformation\\"+str(re.split("[^\w\d]", container)[0])+".csv")):
        with open(path+"ContainerInformation\\"+str(re.split("[^\w\d]", container)[0])+".csv") as containerInfo:
            reader = csv.reader(containerInfo)
            next(reader)

            for row in reader:
                if(row[0].find("Provisional moves not found, please feel free to use Contact Support link for more information")!= -1):
                    continue
                postJson = copy.deepcopy(baseInfo.shipmentEventBase)
                postJson["unitId"] = container
                postJson["location"] = row[3].replace("Accessible text","")
                postJson["city"] = postJson["location"].split(",")[0]
                postJson["eventTime"] = datetime.datetime.strptime(row[0], '%a %d %b %Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
                postJson["vessel"] = str(row[4])
                postJson["voyageNumber"] = str(row[5])
                postJson["unitType"] = row[6]
                postJson["eventName"], postJson["eventCode"] = CMACGMEventTranslate(row[2])
                postJson["resolvedEventSource"] = "CMACGM RPA"
                postJson["codeType"] = "UNLOCODE"
                postJson["reportSource"] = "Ocean Carrier"
                if(postJson["eventCode"] == None):
                    continue
                if(datetime.datetime.strptime(postJson["eventTime"], '%Y-%m-%d %H:%M:%S') > datetime.datetime.now()):
                    postJson["estimatedEvent"] = True
                if(row[7].strip()=="True"):
                    postJson["estimatedEvent"] = True
                print(json.dumps(postJson))
                producer = kafka.KafkaProducer(bootstrap_servers=['10.138.0.2:9092'],
                                    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                                    linger_ms = 10)
                producer.send('RAW_EVENT_RPA_OCEANCARIER_QA', value=postJson)
                producer.flush()

    return

def testMain(container): #test main
    path=""
    for x in os.getcwd().split("\\"):
        path+=x+"\\\\"
    CMACGMPost(container, path)

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    containerList = list(set(containerList))
    for container in containerList:
        CMACGMPost(container, path)

if __name__ == "__main__":
    #testMain(sys.argv[1])
    main(sys.argv[1], sys.argv[2])
