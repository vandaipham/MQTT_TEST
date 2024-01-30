# How to setup Mosquitto MQTT Broker using docker 
These instructions will work on any Debian based OS including Ubuntu, RaspberryPi, WSL2 etc...  
(For non-Debian distros, commands for installation need to be tweaked)  
_By default the config allows only to use local connections for security reasons but since authentication is enabled below, that's not the case._

## 1. Install docker

Latest instructions are [here](https://docs.docker.com/engine/install/ubuntu/) on docker website.  
You can also use this script - [install-docker.sh](/install-docker.sh)


## 2. Create Mosquitto password file - pwfile

```bash
cd mqtt5broker
touch config/pwfile
```

## 3. Create and run docker container for MQTT Broker

```bash
# In case you don't have docker-compose you can install it
sudo apt install docker-compose

# Run the docker container for mqtt
sudo docker-compose -p mqtt5broker up -d

```

### Check if the container is up and working (note down container-id)

```bash

sudo docker ps

```

## 4. Create a user/password in the pwfile

```bash

# login interactively into the mqtt container
sudo docker exec -it <container-id> sh

# add user and it will prompt for password
mosquitto_passwd -c /mosquitto/config/pwfile <yourID>

# delete user command format
mosquitto_passwd -D /mosquitto/config/pwfile <user-name-to-delete>

# type 'exit' to exit out of docker container prompt

```
Then restart the container 
```bash
sudo docker restart <container-id>
```

## 5. Time to test !!!

### Install mosquitto client tools for testing
```bash

sudo apt install mosquitto-clients

```

### Let us start Subscriber now - topic name => 'hello/topic'

```bash

# Without authentication
mosquitto_sub -v -t 'hello/topic'

# With authentication
mosquitto_sub -v -t 'hello/topic' -u <yourID> -P <password>

```

### Let us start Publising to that topic

```bash

# Without authentication
mosquitto_pub -t 'hello/topic' -m 'hello MQTT'

# With authentication
mosquitto_pub -t 'hello/topic' -m 'hello MQTT' -u <yourID> -P <password>

```
## You can also install a nice MQTT Web Client
Read more about it here => https://mqttx.app/  

```bash
sudo docker run -d --name mqttx-web -p 80:80 emqx/mqttx-web
```

## 6. Run IoTNode.py to test !!!
We publish simulated temperature, humidity and light sensor data.
And we subscribe topics to receive commands to control **lamp1**, **lamp2**, **lamp3**.

```bash
# install paho-mqtt to communicate with MQTT broker
pip install paho-mqtt

# run IoTNode.py
python IoTNode.py
```

## Source/Reference for Mosquitto
Github => https://github.com/eclipse/mosquitto