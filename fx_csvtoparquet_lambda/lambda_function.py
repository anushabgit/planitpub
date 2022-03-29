import json
import boto3

def lambda_handler(event, context):
    
    client = boto3.client('glue')
    client.start_job_run(
        JobName = 'csvtoparquetcustom',
        Arguments = {} )
    print("Fx trigger once file loaded to Landing")
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }