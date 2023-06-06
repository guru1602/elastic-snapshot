import boto3
import requests
from requests_aws4auth import AWS4Auth
import os
from requests_aws4auth import AWS4Auth
from dotenv import load_dotenv

load_dotenv() 

access_key      = os.getenv('AWS_ACCESS_KEY_ID')
access_key      = os.getenv('AWS_SECRET_ACCESS_KEY')
region          = os.getenv('AWS_REGION')
host            = os.getenv('ELASTIC_HOST_NAME')
repository_name = os.getenv('REPOSITORY_NAME')
bucket          = os.getenv('AWS_S3_BUCKET')
role            = os.getenv('IAM_SNAPSHOT_ROLE')
api_path        = os.getenv('API_CALL_PATH')
service         = 'es'

credentials = boto3.Session().get_credentials()
awsauth     = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Register repository
path = '_snapshot/%s' % (repository_name) # the OpenSearch API endpoint
url  = host + path

payload = {
 "type": "s3",
 "settings": {
 "bucket": bucket,
 "region": region,
 "role_arn": role
  }
}

headers = {"Content-Type": "application/json"}

# registers repo
r = requests.put(url, auth=awsauth, json=payload, headers=headers)

print(r.status_code)
print(r.text)

# makes get api calls for elastic depending the call passed in API_CALL_PATH
geturl = "%s/%s" %(host, api_path)
g = requests.get(geturl, auth=awsauth, headers=headers)

print(g.status_code)
print(g.text)
