import json
import boto3
import time

# athena constant
DATABASE = 'testing_planit'
TABLE_LAND = 'landing_csv'
TABLE_CONF = 'confirming_parquet'

# S3 constant
S3_OUTPUT = 's3://landingcsvqueryresult/assertresult/'
# S3_BUCKET = 'your_athena_query_output_backet_name'

# number of retries
RETRY_COUNT = 5

def lambda_handler(event, context):
    
    # created query FOR landing
    query_land = "SELECT COUNT (*) FROM %s.%s;" % (DATABASE, TABLE_LAND)
    
    
    # created query FOR conforming
    query_conform = "SELECT COUNT (*) FROM %s.%s;" % (DATABASE, TABLE_CONF)
    
    client = boto3.client('athena')
    
    # Execution 
    response_land = client.start_query_execution(
        QueryString=query_land,
        QueryExecutionContext={
            'Database': DATABASE
        },
        ResultConfiguration={
            'OutputLocation': S3_OUTPUT,
        }
    )
    
    response_conf = client.start_query_execution(
        QueryString=query_conform,
        QueryExecutionContext={
            'Database': DATABASE
        },
        ResultConfiguration={
            'OutputLocation': S3_OUTPUT,
        }
    )
   
   # get query execution id 
    query_execution_id_land = response_land['QueryExecutionId']
    # print(query_execution_id_land) 
    
    query_execution_id_conf = response_conf['QueryExecutionId']
    # print(query_execution_id_conf)
    
    
    # get execution status--landing
    for i in range(1, 1 + RETRY_COUNT):

        # get query execution
        query_status = client.get_query_execution(QueryExecutionId=query_execution_id_land)
        query_execution_status = query_status['QueryExecution']['Status']['State']

        if query_execution_status == 'SUCCEEDED':
            print("LANDING STATUS:" + query_execution_status)
            break

        if query_execution_status == 'FAILED':
            raise Exception("LANDING STATUS:" + query_execution_status)

        else:
            print("LANDING STATUS:" + query_execution_status)
            time.sleep(i)
    else:
        client.stop_query_execution(QueryExecutionId=query_execution_id_land)
        raise Exception('TIME OVER')
        
    # check for query execution status - as this may not have completed after immediate execution
    # get execution status--conforming
    for i in range(1, 1 + RETRY_COUNT):

        # get query execution
        query_status = client.get_query_execution(QueryExecutionId=query_execution_id_conf)
        query_execution_status = query_status['QueryExecution']['Status']['State']

        if query_execution_status == 'SUCCEEDED':
            print("CONFIRMING STATUS:" + query_execution_status)
            break

        if query_execution_status == 'FAILED':
            raise Exception("CONFIRMING STATUS:" + query_execution_status)

        else:
            print("CONFIRMING STATUS:" + query_execution_status)
            time.sleep(i)
    else:
        client.stop_query_execution(QueryExecutionId=query_execution_id_conf)
        raise Exception('TIME OVER')
        
    
    # get query results--land
    result_land = client.get_query_results(QueryExecutionId=query_execution_id_land)
    # print(result_land)
    
    # get query results--conf
    result_conf = client.get_query_results(QueryExecutionId=query_execution_id_conf)
    # print(result_conf)

    # get data--land
    if len(result_land['ResultSet']['Rows']) == 2:

        rowcnt_land = result_land['ResultSet']['Rows'][1]['Data'][0]['VarCharValue']
        print("Landing CSV count : " +rowcnt_land)
        # return rowcnt_land

    else:
        return None
        
    # get data--conf
    if len(result_conf['ResultSet']['Rows']) == 2:

        rowcnt_conf = result_conf['ResultSet']['Rows'][1]['Data'][0]['VarCharValue']
        print("Conforming PARQUET count : " +rowcnt_conf)
        # return rowcnt_land

    else:
        return None    
        
    if rowcnt_land == rowcnt_conf:
        print("Success - Record count matching")
        
    else:
        print("Fail - Record count not matching!!")
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Completed Assertion process step')
    }
