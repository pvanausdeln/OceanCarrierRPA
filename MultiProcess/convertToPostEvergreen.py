import os
import sys
import json
import copy
import requests
import datetime
import glob
import csv
import string
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

    StatusMapEvergreen = {
        "Gate out empty": "OA",
        "Gate in empty": "I",
        "Vessel departed": "VD",
        "Vessel arrived": "VA",
        "Loaded": "AE",
        "loaded on vessel": "AE",
        "Discharged": "UV",
        "Received": "CO",
        "Pick-up by merchant haulage": "MH",
        "Empty container received": "EE",
        "Empty container returned": "RD",
        "Despatched by rail" : "RL",
        "JUNCTION RECEIVED" : "IT"
    }

def EvergreenCodeToName(code):
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
    elif(code == "CO"):
        return "Cargo Received"
    elif(code == "RD"):
        return "Return Container"
    elif(code=="RL"):
        return "Rail Departure"
    elif(code=="IT"):
        return "In Transit"
    return None

def EvergreenEventTranslate(event):
    for key, value in baseInfo.StatusMapEvergreen.items():
        if(event.find(key) != -1):
            return value, EvergreenCodeToName(value)
    return (None, None)



def EvergreenPost(container, path):
    if(os.path.isfile(path+"ContainerInformation\\"+container+".json")):
        with open(path+"ContainerInformation\\"+container+".json") as containerInfo:
            data = json.load(containerInfo)
            postJson = copy.deepcopy(baseInfo.shipmentEventBase)
            postJson["unitId"] = container
            postJson["location"] = data.get("Location")
            postJson["unitSize"] = data.get("Size/Type").split("'")[0]
            postJson["city"] = data.get("Location").split(" ")[0]
            if(len(data.get("Location").split(" ")) > 1):
                postJson["country"] = data.get("Location").split(" ")[1].strip("()")
            postJson["eventTime"] = datetime.datetime.strptime(data.get("Date").title(), '%b-%d-%Y').strftime('%Y-%m-%d %H:%M:%S')
            
            postJson["vessel"] = data.get("Vessel")
            postJson["voyageNumber"] = data.get("Vessel")
                
            postJson["eventCode"], postJson["eventName"] = EvergreenEventTranslate(data.get("Container Moves"))
            postJson["resolvedEventSource"] = "Evergreen RPA"
            postJson["codeType"] = "UNLOCODE"
            postJson["reportSource"] = "Ocean Carrier"
            if(postJson["eventCode"] == None):
                return
            if(datetime.datetime.strptime(postJson["eventTime"], '%Y-%m-%d %H:%M:%S') > datetime.datetime.now()):
                postJson["estimatedEvent"] = True
            print(json.dumps(postJson))
            producer = kafka.KafkaProducer(bootstrap_servers=['10.138.0.2:9092'],
                                    value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                                    linger_ms = 10)
            producer.send('RAW_EVENT_RPA_OCEANCARIER_QA', value=postJson)
            producer.flush()
    return

def testMain(container):
    path=""
    for x in os.getcwd().split("\\"):
        path+=x+"\\\\"
    EvergreenPost(container, path)

def main(containerList, cwd):
    path=""
    for x in cwd.split("\\"):
        path+=x+"\\\\"
    containerList = list(set(containerList))
    for container in containerList:
        x=EvergreenPost(container, path)
    
if __name__ == "__main__":
    #testMain(sys.argv[1])
    main(sys.argv[1], sys.argv[2])
