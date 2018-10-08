# AstroPlant-Mainflux 

### Mainflux
Please refer to https://mainflux.readthedocs.io/en/latest/ to learn about Mainflux.

Three core concepts of Mainflux (MF):
  - User. A human user of the system. Management that includes creating, editing and deleting channels and things.
  - Thing. A physical device or application. 
     - ID
     - Owner (the user who created them)
     - Type (application or device)
     - Key (unique identifier)
  - Channel. Connecting layer of connecting things
    - ID
    - Owner
    - List of connected things. Only the Things connected to the same channel can communicate with each other.

Mainflux is based on docker containers and functions as a set of microservices exposed through API's. We can use Mainflux as our "data server" and interface with it through custom built applications to implement AstroPlant's Data Model (see: https://www.astroplant.io/astroplant-data-model/). 

### AstroPlant-Mainflux concept
This repository should contain three microservices to interface with Mainflux. The following services are described below:
  - [Under development] *AstroPlant-Mainflux client application*. A docker-based Rest-Flask application with a React front-end that supports Mainflux provisioning. A MF user can register through this application and setup its AstroPlant system including sensor configurations. 
    - *Provision devices*. A phyisical device can be provisioned e.g. a RPi-client through the MF API. An "mf-application" + "mf-channel" should be automatically setup at the point a user provisioned its device. In AstroPlant terms each kit is an MF device and is provisioned through this client application. A device token and channel ID is displayed for further use in the device-client application. 
    - *Database*. A relational database is used for further astroplant datamodel implementation, linking MF things with users and data. The connected database stores the following Mainflux specifics:
        - username, password, user token, provisioned devices
        - Each provisioned device is linked to its own unique Mainflux channel and application (application is for actuator control and manual input)
    - *Actuator control and manual input*. Once a device is provisioned and an AstroPlant project is initiated, an interface is available for actuator control and manual input. Actuator messages can be send over HTTP to MF-channels. The device client can handle these messages for scheduling actions, namely scheduled GPIO on/off messages as well as PWM. Manual input is considered data that cannot be automated by the AstroPlant-Mainflux device, such as number of leafs, plant weight and root length. Manual input is similarly transmitted although the AstroPlant-Mainflux device is not listening to these messages, but this information is stored in the MF-database. 
  - [TO DO] *AstroPlant-Mainflux data service*. As raw data is stored in Influx DB on the MF data-server queries have to be made to retrieve bulk data or link data to given projects/experiments. A dedicated service is needed to provide this data and make them available for dashboard display or export.  The Mainflux DB reader API can be used for this purpose.
  - [TO DO] *Device client/AstroPlant-Mainflux device*. Similarly to the prototype implementation of AstroPlant, a MF-device/AstroPlant-kit needs to know what sensors are configured before transmission of data. It also needs a service running for actuator control. Potentially sensor data is not send everytime a sensors captures the data, this might happen in set time intervals and sending averages over the time period. 
    - *Device messages*. Messages are formatted in the MF SenML format (see: http://www.elastetic.com/wp/2018/05/20/senml-messages/). They are send over the channel and each device has its unique channel id and device token for transmission. Depending on the device implementation websockets, http, mqtt may be used for data transmission.
    - *Actuator control*. A listener needs to be inplace to listen to actuator messages on the mf channel. In turn a scheduler should be activated. 

### Missing implementation and side notes:
Aside from these three services, a missing implementation is camera image transmission. Possibly a seperate service and data storage is needed for images, while still using Mainflux message system to denote when images are send and where they are stored.
Another point is the creation of a mobile app, ideally the mobile app does not interact directly with Mainflux.  Instead the mobile app should interface with the *AstroPlant-Mainflux client application*.

### Setup Mainflux
It is recommended to follow the read the docs or the following tutorial: https://medium.com/mainflux-iot-platform/mainflux-open-source-iot-platform-set-up-and-usage-70bed698791a

Prerequisites:
  - Git
  - Docker
  - Docker compose


```sh
$ git clone https://github.com/mainflux/mainflux.git
```
Start the influxDb writer & reader + the normal core services: 
```sh
docker-compose -f docker/docker-compose.yml -f docker/addons/influxdb-writer/docker-compose.yml -f docker/addons/influxdb-reader/docker-compose.yml up -d
```

### Setup AstroPlant-Mainflux client application
```sh
$ git clone https://github.com/SidneyNiccolson/APMainflux.git
```
Install all_requirements.txt and build the container and run the service:
```sh
docker-compose -f docker-compose-dev.yml up -d --build
```

(optional) Run unit test:
```sh
docker-compose -f docker-compose-dev.yml run users python manage.py test
```

Go to http://localhost:5001/users/ping to check if service is running

### example mainflux script
In the device_client folder a simple example script is available to test certain features of mainflux.

