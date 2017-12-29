# Installation
Some rows of this documentation are suitable only for ubuntu operating system

#### Install packages
```
$ sudo apt-get install git
$ sudo apt-get install python-pip
$ sudo apt-get install python3-venv
```

#### Git repository
```
$ git clone https://github.com/Empressive/intranet-tasks.git
$ cd intranet-tasks
```

#### Virtual enironment
```
$ python3.5 -m venv .env
$ source ./env/bin/activate
```

#### Pip packages
```
(.env)$ pip install -r requirements.txt
```

#### Launching
```
(.env)$ python3 manage.py test
(.env)$ python3 manage.py runserver
```

#### Tasks
| Task  | URL |
| ------------- | ------------- |
| Front-end  | http://127.0.0.1:8000/  |
| API  | http://127.0.0.1:8000/api/  |
| Javascript  | http://127.0.0.1:8000/vocabulary/  |


#### API
| Parameter  | Type | Case-insensitive | Description |
| ------------- | ------------- | ------------- | ------------- |
| name  | Text | False | Full match of the text in the name field |
| description | Text | True | Full match of the word in the description field |
| is_done | Boolean | True | Can take values (1, 0, true, false, True, False) |
| priority | Text | False | Can take values (Low, Normal, High) |
| parent | Text | True | Partial match of the name of the parent |