import boto3
import requests
import datetime
import os
from requests_aws4auth import AWS4Auth
from dotenv import load_dotenv

load_dotenv() 

access_key          = os.getenv('AWS_ACCESS_KEY_ID')
access_key          = os.getenv('AWS_SECRET_ACCESS_KEY')
region              = os.getenv('AWS_REGION')
host                = os.getenv('ELASTIC_HOST_NAME') 
elastic_search_name = os.getenv('ELASTIC_SEARCH_NAME')
repository_name     = os.getenv('REPOSITORY_NAME')
service             = 'es'

credentials = boto3.Session().get_credentials()
awsauth     = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# set time for snapshot 
t     = datetime.datetime.now()
today = (t.strftime("%Y-%m-%d-%H:%M"))

# set snapshot name,url 
snapshot_name = "%s-%s" %(elastic_search_name, today)
snapurl       = "%s/_snapshot/%s/%s" % (host, repository_name, snapshot_name)
querystring   = {"pretty":"","wait_for_completion":"true"}

payload = {
  "ignore_unavailable": "true",
  "include_global_state": "false"
}

headers = {"Content-Type": "application/json"}

print("Starting Snapshot: %s" %(snapshot_name))

s = requests.put(snapurl, auth=awsauth, json=payload, headers=headers, params=querystring)
if s.status_code == 200:
    print("Created Snapshot: %s in Repository: %s" % (snapshot_name, repository_name))
elif s.status_code == 504:
    print("Snapshot is in Progress Wait for sometime and continue...")
    datetime.sleep(180)
