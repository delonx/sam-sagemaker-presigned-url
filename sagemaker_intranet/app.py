import boto3
import json

# import requests


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    sagemaker_client = boto3.client('sagemaker')

    if 'queryStringParameters' not in event or 'userprofile' not in event['queryStringParameters']:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "lack parameter: userprofile"
            }),
        }
        
    user_profile_name = event['queryStringParameters']['userprofile']
    response = sagemaker_client.create_presigned_domain_url(
        DomainId='[placeholder for sagemaker studio domain id]',
        UserProfileName=user_profile_name
        # SessionExpirationDurationInSeconds=123,
        # ExpiresInSeconds=123
    )
    authorized_url = response['AuthorizedUrl']

    return {
        "statusCode": 200,
        "body": json.dumps({
            "sagemaker_domain_presigned_url": authorized_url,
            # "location": ip.text.replace("\n", "")
        }),
    }
