#######################################################################################
# Yourname: Pongpisut Tupwong
# Your student ID: 66070124
# Your GitHub Repo: https://github.com/PongpisutFlook/IPA2025-Final

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.

import os
import time
import json
import requests
from dotenv import load_dotenv
from requests_toolbelt.multipart.encoder import MultipartEncoder

from restconf_final import (
    create as rest_create,
    delete as rest_delete,
    enable as rest_enable,
    disable as rest_disable,
    status as rest_status
)

# from netmiko_final import (
#     create as net_create,
#     delete as net_delete,
#     enable as net_enable,
#     disable as net_disable,
#     status as net_status
# )
from netmiko_final import gigabit_status
from ansible_final import showrun
import glob



#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

load_dotenv()

ACCESS_TOKEN = os.environ["WEBX_ACCESS_TOKEN"]

ip = {"10.0.15.61", "10.0.15.62", "10.0.15.63", "10.0.15.64", "10.0.15.65"}
method = ''

#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = (
    os.environ["ROOM_ID"]
)

while True:
    # always add 1 second of delay to the loop to not go over a rate limit of API calls
    time.sleep(1)

    # the Webex Teams GET parameters
    #  "roomId" is the ID of the selected room
    #  "max": 1  limits to get only the very last message in the room
    getParameters = {"roomId": roomIdToGetMessages, "max": 1}

    # the Webex Teams HTTP header, including the Authoriztion
    getHTTPHeader = {"Authorization": "Bearer " + ACCESS_TOKEN}

# 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
    
    # Send a GET request to the Webex Teams messages API.
    # - Use the GetParameters to get only the latest message.
    # - Store the message in the "r" variable.
    r = requests.get(
        "https://webexapis.com/v1/messages",
        params=getParameters,
        headers=getHTTPHeader,
    )
    # verify if the retuned HTTP status code is 200/OK
    if not r.status_code == 200:
        raise Exception(
            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
        )

    # get the JSON formatted returned data
    json_data = r.json()

    # check if there are any messages in the "items" array
    if len(json_data["items"]) == 0:
        raise Exception("There are no messages in the room.")

    # store the array of messages
    messages = json_data["items"]
    
    # store the text of the first message in the array
    message = messages[0]["text"]
   
    message_parts = message.strip().split()
    print(message_parts)

    # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
    #  e.g.  "/66070123 create"
    if message_parts[0] == "/66070124":

        # extract the command
        command = message.split(" ", 1)[1]
        print(command)

# 5. Complete the logic for each command

        if message_parts[1] == "restconf":
            method = "restconf"
            responseMessage = "Ok: Restconf"
        elif message_parts[1] == "netconf":
            method = "netconf"
            responseMessage = "Ok: Netconf"
        elif method == '':
            responseMessage = "Error: No method specified"

        elif message_parts[1] in ["create", "delete", "enable", "disable", "status", "gigabit_status", "showrun"]:
            if len(message_parts) < 3:
                responseMessage = "Error: No IP specified"
            else:
                pass
        elif message_parts[1] not in ip:
            responseMessage = "Error: Unknown IP"
        elif message_parts[2] == "gigabit_status":
            responseMessage = gigabit_status(message_parts[1])
        elif message_parts[2] == "showrun":
            responseMessage = showrun()
        elif method == "restconf":
            if message_parts[2] == "create":
                responseMessage = rest_create(message_parts[1], "66070124")
            elif message_parts[2]== "delete":
                responseMessage = rest_delete(message_parts[1], "66070124")
            elif message_parts[2] == "enable":
                responseMessage = rest_enable(message_parts[1], "66070124")
            elif message_parts[2] == "disable":
                responseMessage = rest_disable(message_parts[1], "66070124")
            elif message_parts[2] == "status":
                responseMessage = rest_status(message_parts[1], "66070124")
        else:
            responseMessage = "Error: No command found."
        print(method)
# 6. Complete the code to post the message to the Webex Teams room.

        # The Webex Teams POST JSON data for command showrun
        # - "roomId" is is ID of the selected room
        # - "text": is always "show running config"
        # - "files": is a tuple of filename, fileobject, and filetype.

        # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
        
        # Prepare postData and HTTPHeaders for command showrun
        # Need to attach file if responseMessage is 'ok'; 
        # Read Send a Message with Attachments Local File Attachments
        # https://developer.webex.com/docs/basics for more detail

        if command == "showrun" and responseMessage == 'ok':
            filename = glob.glob("show_run_*.txt")
            filename = max(filename, key=os.path.getctime)
            fileobject = open(filename, "rb")
            filetype = "text/plain"
            postData = {
                "roomId": roomIdToGetMessages,
                "text": "show running config",
                "files": (filename, fileobject, filetype),
            }
            postData = MultipartEncoder(postData)
            HTTPHeaders = {
                "Authorization": "Bearer " + ACCESS_TOKEN,
                "Content-Type": postData.content_type,
            }
        # other commands only send text, or no attached file.
        else:
            postData =  {"roomId": roomIdToGetMessages, "text": responseMessage}
            postData = json.dumps(postData)

            # the Webex Teams HTTP headers, including the Authoriztion and Content-Type
            HTTPHeaders = {
                "Authorization": "Bearer " + ACCESS_TOKEN,
                "Content-Type": "application/json"
            }

        # Post the call to the Webex Teams message API.
        r = requests.post(
            "https://webexapis.com/v1/messages",
            data=postData,
            headers=HTTPHeaders,
        )
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )
