import requests
import urllib.parse
"""
A basic example of a python web-app communicating with Mainflux
"""
# local pc mainflux address
BROKER_ADDRESS = "https://127.0.0.1/"
USERNAME = "<myusername>"
PASSWORD = "<mypassword>"
# Mainflux application name
# Should be linked to device token as the channel to communicate should be unique if users own multiple devices
APPLICATION_NAME = "Actuator-controller_"
# Mainflux channel name
# Should be linked to device token as the channel to communicate should be unique if users own multiple devices
CHANNEL_NAME = "AstroPlant-channel_"


def test_options():
    options = ["phase 1 > Provision device", "phase 2 > Connect default device to default channel", "quit"]
    print("***This simple app is for starting development with Mainflux. \n We assume in this case that users are "
          "already registered (e.g. username and password are available).***\n")
    print("Depending on what state the hypothetical application is in, we need to chose the following modes:")
    # Print out your options
    for i in range(len(options)):
        print(str(i + 1) + ":", options[i])
    while True:
        # Take user input and get the corresponding item from the list
        inp = int(input("Enter a number: "))
        if inp in range(1, 4):
            return inp
        else:
            print('invalid input')


""" Test request

    Pretty prints a Request object
    
    Args:
        req (Request object): a given http request object

"""


def print_request(req):
    print('HTTP/1.1 {method} {url}\n{headers}\n\n{body}'.format(
        method=req.method,
        url=req.url,
        headers='\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        body=req.body,
    ))


""" Retrieves the user token

    Used for provisioning
    
    Returns:
        dict: token as key and value the registered token from the user
"""


def get_token():
    try:
        print("obtaining token...")
        r = requests.post(urllib.parse.urljoin(BROKER_ADDRESS, 'tokens'),
                          json=({'email': USERNAME, 'password': PASSWORD}), verify=False)
        if r.status_code == 201:
            return r.json()
        else:
            # TODO change to loggers
            raise SystemExit("Failed to retrieve token, HTTP status code: " + str(r.status_code))
    except Exception as e:
        print("could not obtain token :"+str(e))


""" Provisions a device

    A device needs to be able to send and retrieve messages over channels through a provisioned 'virtual' device

    Args:
        device_name (str): Name given by user
        user_token (dict): User token
    Returns:
        int: status code
"""


def provision_device(device_name, user_token):
    headers = {'content-type': 'application/json', 'Authorization': user_token['token']}
    try:
        print("Provisioning device: " + device_name + "...")
        r = requests.post(urllib.parse.urljoin(BROKER_ADDRESS, 'things'),
                          json=({'type': 'device', 'name': device_name}), verify=False, headers=headers)
        if r.status_code == 201:
            print("device provisioned...")
            return r.status_code
        else:
            # TODO change to loggers
            raise SystemExit("Failed to provision device, HTTP status code: " + str(r.status_code))
    except Exception as e:
        print("could not provision device :"+str(e))


""" Provisions an application 

    A default application that is connected to devices on the same channel for actuator support 

    Args:
        user_token (dict): User token
    Returns:
        str: unique application name
"""


def provision_application(user_token, device_id):
    headers = {'content-type': 'application/json', 'Authorization': user_token['token']}
    try:
        print("[AUTO] Provisioning application...")
        r = requests.post(urllib.parse.urljoin(BROKER_ADDRESS, 'things'),
                          json=({'type': 'app', 'name': APPLICATION_NAME + str(device_id)}), verify=False, headers=headers)
        if r.status_code == 201:
            print("[AUTO] application provisioned...")
            return APPLICATION_NAME + str(device_id)
        else:
            # TODO change to loggers
            raise SystemExit("Failed to provision application, HTTP status code: " + str(r.status_code))
    except Exception as e:
        print("could not provision application :"+str(e))


""" Provisions a channel

    A default channel that is connected to devices on the same channel for actuator support 

    Args:
        user_token (dict): User token
    Returns:
        str: unique channel name
"""


def provision_channel(user_token, device_id):
    headers = {'content-type': 'application/json', 'Authorization': user_token['token']}
    try:
        print("[AUTO] Provisioning channel...")
        r = requests.post(urllib.parse.urljoin(BROKER_ADDRESS, 'channels'),
                          json=({'name': CHANNEL_NAME + str(device_id)}), verify=False, headers=headers)
        if r.status_code == 201:
            print("[AUTO] channel provisioned...")
            return CHANNEL_NAME + str(device_id)
        else:
            # TODO change to loggers
            raise SystemExit("Failed to provision channel, HTTP status code: " + str(r.status_code))
    except Exception as e:
        print("could not provision channel :"+str(e))


def get_channels(user_token):
    headers = {'content-type': 'application/json', 'Authorization': user_token['token']}
    try:
        print("Retrieving channels...")
        r = requests.get(urllib.parse.urljoin(BROKER_ADDRESS, 'channels'), verify=False, headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            # TODO change to loggers
            raise SystemExit("Failed to retrieve channels, HTTP status code: " + str(r.status_code))
    except Exception as e:
        print("could not get channels :"+str(e))


def connect_channel(channel_id, device_id, user_token):
    headers = {'Authorization': user_token['token']}
    try:
        print("Connecting channel...")
        url = BROKER_ADDRESS + 'channels/' + str(channel_id) + '/things/' + str(device_id)
        r = requests.put(url, verify=False, headers=headers)
        if r.status_code == 200:
            return "Channel provisioned..."
        else:
            # TODO change to loggers
            raise SystemExit("Failed to connect channel, HTTP status code: " + str(r.status_code))
    except Exception as e:
        print("could not provision channel :"+str(e))


""" Retrieves devices connected to users

    Get user connected Things

    Args:
        address (str): Address of mainflux server
        user_token (dict): User token
    Returns:
        int: status code
"""


def get_connected_things(user_token):
    headers = {'content-type': 'application/json', 'Authorization': user_token['token']}
    try:
        print("Retrieving connected devices")
        r = requests.get(urllib.parse.urljoin(BROKER_ADDRESS, 'things'), verify=False, headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            # TODO change to loggers
            raise SystemExit("Failed to retrieve connected devices, HTTP status code: " + str(r.status_code))
    except Exception as e:
        print("could not provision application :"+str(e))


""" Retrieves default applications connected to users

    Get user AP specific device id

    Args:
        name (str): name of device
    Returns:
        int: id of device
"""


def get_default_app_info(user_token):
    all_things = get_connected_things(user_token)
    for things in all_things["things"]:
        if things["type"] == 'app' and things['name'] == APPLICATION_NAME:
            id = things["id"]
            key = things["key"]
            return id, key


""" Retrieves devices connected to users

    Get user AP specific device id

    Args:
        name (str): name of device
    Returns:
        int: id of device
"""


def get_default_device_info(name, user_token):
    all_things = get_connected_things(user_token)
    for things in all_things["things"]:
        if things["type"] == 'device' and things['name'] == name:
            id = things["id"]
            key = things["key"]
            return id,key


def get_default_channel_id(user_token):
    channels = get_channels(user_token)
    for channel in channels["channels"]:
        if channel["name"] == CHANNEL_NAME:
            id = channel["id"]
            return id


if __name__ == "__main__":
    # retrieve user_token
    user_token = get_token()
    while True:
        mode = test_options()
        if "token" in user_token:
                print("user token received: "+user_token['token']+"...")
                if mode == 1:
                    dname = input("What is your device name: ")
                    # provision a device
                    provision_device(dname, user_token)
                    device_id, device_token = get_default_device_info(dname, user_token)
                    APPLICATION_NAME = provision_application(user_token, device_id)
                    CHANNEL_NAME = provision_channel(user_token, device_id)
                elif mode == 2:
                    name = input("enter device name: ")
                    device_id, device_token = get_default_device_info(name, user_token)
                    app_id, app_token = get_default_app_info(user_token)
                    channel_id = get_default_channel_id(user_token)
                    print("connecting your device to default channel...")
                    connect_channel(channel_id,device_id, user_token)
                    print("[AUTO] connecting default application to default channel...")
                    connect_channel(channel_id, app_id, user_token)
                elif mode == 3:
                    raise SystemExit("Program exited...")


        else:
            raise SystemExit("provisioning failed, could not retrieve user token")



