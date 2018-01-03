# Introduction

This script (init_db.py) is used to initialize mongodb for xapi-service. It is intend to initialize from an empty database, for update purpose, you can find the useful part in this script.

## Usage

1. Clone this repo.

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Change the following parameters at the top of this script.

```py
DB_CONNECTION = 'mongodb://localhost:27017/'
DB_NAME = 'xapi-server'

ORG = 'Default Organisation'
LRS = 'Default LRS'
CLIENT = 'Default Client'
AUTHORITY_EMAIL = 'admin@xapi.site'
BASIC_KEY = 'CHANGETHISSTRINGWITH40LETTERS01234567890'
BASIC_SECRET = 'CHANGETHISSTRINGWITH40LETTERS01234567890'
```

4. Execute the script. Note that the script will stop if the database already exist.

```bash
python3 init_db.py
```
