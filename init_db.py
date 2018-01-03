import datetime, pymongo

# ======== Change the following variables base on your requirements ========

DB_CONNECTION = 'mongodb://localhost:27017/'
DB_NAME = 'xapi-server'

ORG = 'Default Organisation'
LRS = 'Default LRS'
CLIENT = 'Default Client'
AUTHORITY_EMAIL = 'admin@xapi.site'
BASIC_KEY = 'CHANGETHISSTRINGWITH40LETTERS01234567890'
BASIC_SECRET = 'CHANGETHISSTRINGWITH40LETTERS01234567890'

# ======== For general usage you DO NOT need to change the following code ========

def main():
  # Connect to mongodb
  client = pymongo.MongoClient(DB_CONNECTION)

  # Exist if database already exists
  db_names = client.database_names()
  if(DB_NAME in db_names):
    print(f"Database {DB_NAME} already exists.")
    return

  # Create new database
  db = client[DB_NAME]

  # ======== Create and initialize organisations ========
  org = {
    "name" : ORG,
    "createdAt" : datetime.datetime.utcnow(),
    "updatedAt" : datetime.datetime.utcnow()
  }

  org_id = db.organisations.insert_one(org).inserted_id

  print(f"Org created. Default Org: ${org_id}")

  # ======== Create and initialize lrs ========
  db.lrs.ensure_index('organisation', pymongo.ASCENDING)

  lrs = {
    "title" : LRS,
    "organisation" : org_id,
    "statementCount" : 0,
    "createdAt" : datetime.datetime.utcnow(),
    "updatedAt" : datetime.datetime.utcnow()
  }

  lrs_id = db.lrs.insert_one(lrs).inserted_id
  print(f"Lrs created. Default Lrs: ${lrs_id}")

  # ======== Create and initialize client ========
  db['client'].ensure_index('organisation', pymongo.ASCENDING)
  db['client'].ensure_index('lrs_id', pymongo.ASCENDING)

  client = {
    "organisation" : org_id,
    "lrs_id" : lrs_id,
    "title" : CLIENT,
    "scopes" : [
      "xapi/all"
    ],
    "isTrusted" : True,
    "authority" : "{\"objectType\":\"Agent\",\"name\":\"admin\",\"mbox\":\"" + AUTHORITY_EMAIL + "\"}",
    "api" : {
      "basic_key" : BASIC_KEY,
      "basic_secret" : BASIC_SECRET
    },
    "createdAt" : datetime.datetime.utcnow(),
    "updatedAt" : datetime.datetime.utcnow()
  }

  client_id = db['client'].insert_one(client).inserted_id
  print(f"Client created. Default Client: ${client_id}")

  # ======== Create and initialize statements ========

  db.statements.ensure_index([
    ('organisation',pymongo.ASCENDING),
    ('timestamp',pymongo.DESCENDING),
    ('_id',pymongo.ASCENDING)
  ])

  print("Statements created.")

  # ======== Create and initialize fullActivities ========
  db.fullActivities.ensure_index([('organisationId',1),('lrsId',1),('activityId',1)])

  print("FullActivities created.")

  print("Initialize complete!")

if(__name__ == '__main__'):
  main()
