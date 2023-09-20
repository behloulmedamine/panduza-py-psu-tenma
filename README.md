# Panduza Python

## Prerequisites

- Windows or Linux
- python3
- pip 

## Requirements
```
sudo apt-get update
sudo apt-get install -y mosquitto git
sudo apt-get install -y python3 python3-pip
sudo pip install -r ./tests/requirements.txt
sudo pip install -r ./platform/requirements.txt
sudo pip install ./client/
```


## Client and Admin Tools Installation

```
sudo python3 ./platform/panduza_platform/__main__.py
```
Or
```
sudo local/platform-dryrun.sh
```
