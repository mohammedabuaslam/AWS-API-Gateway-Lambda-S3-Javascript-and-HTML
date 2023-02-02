import uuid
import json
import boto3
import logging
from custom_encoder import CustomEncoder
import base64 

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = 'product-inventory'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
deleteMethod = 'DELETE'
healthPath = '/health'
productPath = '/product'
productsPath = '/products'

def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == getMethod and path == healthPath:
    	body = {
		'Message': 'SUCCESS',
		'headers': {
            'Access-Control-Allow-Origin': '*'
        },
		}
    	response = buildResponse(200,body)
    elif httpMethod == getMethod and path == productPath:
    	response = getProduct(event['queryStringParameters']['product-id'])
    elif httpMethod == getMethod and path == productsPath:
    	response = getProducts()
    elif httpMethod == postMethod and path == productPath:
    	response = saveProduct(json.loads(event['body']))
    elif httpMethod == patchMethod and path == productPath:
    	requestBody = json.loads(event['body'])
    	response = modifyProduct(requestBody['product-id'],requestBody['updateKey'],requestBody['updateValue'])
    elif httpMethod == deleteMethod and path == productPath:
    	requestBody = json.loads(event['body'])
    	response = deleteProduct(requestBody['product-id'])
    else:
    	response = buildResponse(404, 'Not Found')

    return response

def getProduct(productId):
	try:
		response = table.get_item(
			Key={
				'product-id': productId
			})
		if 'Item' in response:
			return buildResponse(200, response['Item'])
		else:
			return buildResponse(404, {'Message': 'product-id: %s not found' % productId})
	except:
		logger.exception('Do custom error handling here')

def getProducts():
	try:
		response = table.scan()
		result = response['Items']

		while 'LastEvaluatedKey' in response:
			response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
			result.extend(response['Item'])
		body = {
		'products': result
		}
		return buildResponse(200, body)
	except:
		logger.exception("Do custom error handling here")

def saveProduct(requestBody):
	try:
		logger.info(requestBody)
		encoded_string = requestBody['Image_Url']
		if len(encoded_string) % 4 != 0:
			encoded_string += "=" * (4 - len(encoded_string) % 4)
		decoded_string = base64.b64decode(encoded_string)
		fileName = requestBody['fileName']
		# name, extension = fileName.split('.')
		object_name = uuid.uuid4().hex[:10]
		sending_name_and_ext = str(object_name) + '___' + str(fileName)
		client=boto3.client('s3')
		response = client.put_object(Body=decoded_string,Bucket='store-images-for-demo',Key=sending_name_and_ext,)
		requestBody['Image_Url'] = 'https://store-images-for-demo.s3.ap-south-1.amazonaws.com/'+sending_name_and_ext
		table.put_item(Item=requestBody)
		body = {
			'Operation': 'SAVE',
			'Message': 'SUCCESS',
			'Item': requestBody,
			'headers': {
            'Access-Control-Allow-Origin': '*'
        	},
		}
		return buildResponse(200, body)
	except:
		logger.exception("Do custom error handling here")

def modifyProduct(productId, updateKey, updateValue):
	try:
		response = table.update_item(
			Key={
				'product-id': productId
			},
			UpdateExpression='set %s = :value' % updateKey,
			ExpressionAttributeValues={
				':value': updateValue
			},
			ReturnValues='UPDATED_NEW'
		)
		body = {
			'Operation': 'UPDATE',
			'Message': 'SUCCESS',
			'UpdatedAttributes': response
		}
		return buildResponse(200, body)
	except:
		logger.exception("Do custom error handling here")

def deleteProduct(productId):
	try:
		response = table.delete_item(
			Key={
			'product-id': productId
			},
			ReturnValues= 'ALL_OLD'
			)
		body = {
			'Operation': 'DELETE',
			'Message': 'SUCCESS',
			'deletedItem': response
		}
		return buildResponse(200, body)
	except:
		logger.exception("Do custom error handling here")

def buildResponse(statusCode, body=None):
	response = {
		'statusCode': statusCode,
		'headers':{
			'Content-Type': 'application/json',
			'Access-Control-Allow-Origin': '*',
			"x-api-key": "s4EZrDIRXH6FEmpm8rzuo5Y3hPUJpg0S9R5FdW8Z"
		}
	}
	if body:
		response['body'] = json.dumps(body, cls=CustomEncoder)
	return response