import os

IS_OFFLINE = os.environ.get('IS_OFFLINE', default=False)

DYNAMO_DB_PICTURES_TABLE_NAME = os.environ['PICTURES_TABLE_NAME']
