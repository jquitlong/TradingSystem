# Trading API
Trading backend api addresses the usual trading system. Primary features are listed below.
1. User authentication
2. Endpoint for place trades
3. Endpoint for retrieve total value invested

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install virtual environment.

```bash
pip install virtualenv
```

Create and activate the virtual environment.
```bash
virtualenv venv
venv/Scripts/activate
```

Install all the requirements
```bash
pip install -r requirements.txt
```

Go inside the directory up to manage.py level. Then initialize migrate to have initial database setup
```bash
python manage.py migrate
```

Create super user
```bash
python manage.py createsuperuser
```

## Usage

```bash
python manage.py runserver
```

## Test (Build in testing)
Keep the server running and open new console, activate virtual environment

```bash
python manage.py test
```

## API Usage
Read on API Usage PDF
