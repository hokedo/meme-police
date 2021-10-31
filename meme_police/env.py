import os

IS_OFFLINE = os.environ.get('IS_OFFLINE', default=False)

DYNAMO_DB_PICTURES_TABLE_NAME = os.environ['PICTURES_TABLE_NAME']
LOCAL_DYNAMO_DB_PORT = int(os.environ.get('LOCAL_DYNAMO_DB_PORT', default=8010))
