# LightServer
This server is designed to run on an esp32 with a connected light-sensor and deliver the light-level to multiple 
subscribers simultaneously. There is on existing implementation of a client that utilizes the information from this
server to dimm the screen of a PC: https://github.com/enze-l/LightDesktop

***warning:*** The sensor currently saves the connection data for your network in plain text! Do not use this project if you do not understand why this is a security vulnerability!

# Api

This Server mainly offers GET endpoints. The exception to this rule is that clients can register themselves for
receiving the current state continuously and delete themselves from this register again. 

| method | path             | information                                 |
|--------|------------------|---------------------------------------------|
| GET    | /subscriber      | List of current subscribers                 |         
| POST   | /subscriber/\<ip:port> | Subscribe to the sensor to receive readings |         
| DELETE | /subscriber/\<ip:port> | Unsubscribe from the sensor                 |
| GET    | /reading         | Last brightness reading                     |         
| GET    | /reading/min     | All-time lowest reading                     |         
| GET    | /reading/max     | All-time highest reading                    |         
| GET    | /list/day        | List of readings in the last 24 hours       |         
| GET    | /list/100        | List of the last 100 readings               |     

# Setup
- install micropython on your esp32
- copy the files of this repository to the root of the esp32
- create two files with the name "PASSWORD" and "SSID" and fill them with the connection information for your network


# Design
This server utilizes "TinyWeb" (https://github.com/belyalov/tinyweb) for delivering a REST-full API. The used sensor
is a digital sensor with the name bh1750 that can be interfaced with via an i2c-interface. This project uses the
following project to interface with it: https://github.com/PinkInk/upylib/tree/master/bh1750 .
For a lack of intuitiv websocket-library for micropython the server utilized the plain http protocol to send the
current lightning-information to subscribed clients.
