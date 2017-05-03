# Python EWS Notify
Notifies you if any new emails arrive in your exchange account. This is a quickfix for users that can not get
notifications from Outlook Web Access (OWA). This is accomplished by using exchange webservices (ews) and a
notifications library for python.

## Install
* Download or clone this repo

* (Optional) Create a new virtualenv and activate it
```bash
virtualenv -p python3.5 venv 
source venv/bin/activate
```

* Install requirements
```bash
pip install -r requirements.txt
```

* Choose an email notification sound and download it to the current folder
For inspiration, we recommend [http://www.sounds4email.com/sounds/popular.php]()

* Create a credentials file
```bash
cp credentials-example .credentials
nano .credentials # or use any other editor of your choice
```
