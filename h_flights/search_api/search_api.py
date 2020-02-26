import json

# AWS lambda function API
# URL to call that function on AWS lambda
#https://mcrg8lx144.execute-api.us-east-1.amazonaws.com/default/HolidaysFlight?destination=Rome&minDays=3&maxDays=5&travelersNum=2
def lambda_handler(event, context):

    output_data = {}

    try:
        # Get all parameters from query string
        destination = event['queryStringParameters']['destination']
        min_days = event['queryStringParameters']['minDays']
        max_days = event['queryStringParameters']['maxDays']
        travelers_num = event['queryStringParameters']['travelersNum']

        status_code = 200
        output_data['inputParameters'] = {'destination': destination, 'minDays': min_days, 'maxDays': max_days, 'travelersNum' : travelers_num}


    except:
        output_data['status'] = "parameters are incorrect."
        status_code = 400

    return {
        'statusCode': status_code,
        'body': json.dumps(output_data)
    }
     

if __name__ == "__main__":
    query_parameters_debug = {"queryStringParameters": {"destination": "Rome", "minDays": 3,
                                                        "maxDays": 5, "travelersNum": 2}}
    print(lambda_handler(query_parameters_debug, 1))
