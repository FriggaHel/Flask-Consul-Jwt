# How to install modules dependencies and make things work !
* ```virtualenv -p `which python3` venv```
* ```. ./venv/bin/activate```
* ```pip install -r requirements.txt```
* ```python ./app.py```

* You can override some settings through the command-line
  * *EXPOSED_ADDRESS*: Address to register to consul for health check and remote services
    Default: *127.0.0.1*
  * *CONSUL_ADDRESS*: Address used to contact consul Agent
    Default: *127.0.0.1*
  * *APP_NAME*: Name of service
    Default: *app*

# Stack
* Flask
* Flask-Cors
* Flask-SQLAlchemy
* Flask-JWT
* SQLAlchemy
* mysqlclient
* Tornado
* python-consul
