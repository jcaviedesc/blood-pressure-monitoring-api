# tracking-blood-pressure-api
API developed in python with fastapi for tracking blood pressure

## Requirements
- Python 3.10.2+
- [pyenv](https://github.com/pyenv/pyenv)

## Setup virtualenv
to create a virtual environment, I recommend using [pyenv](https://github.com/pyenv/pyenv)
```bash
$ pyenv virtualenv 3.10.2 [name of virtualenv]
```

## Install packages
```bash
$ pip install -r requirements.txt
```
## Run it
In the root directory run:
```bash
$ uvicorn app.main:app --reload
```
