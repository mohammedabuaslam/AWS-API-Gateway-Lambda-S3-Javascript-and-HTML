# AWS REST API, Lambda, DynamoDB and S3 Application

This application provides a solution to process form data, store it in a DynamoDB table and an S3 bucket, and retrieve the data on request. The form data is submitted using an HTML form, processed by an AWS Lambda function (Python), and returned via a REST API endpoint in AWS API Gateway.

## Prerequisites

- An AWS account
- An S3 bucket created in AWS

## Steps

1. Set up AWS account and services: Create an AWS account and set up Amazon S3, Amazon Lambda, Amazon API Gateway, and Amazon DynamoDB.
2. Create an S3 bucket: Create an S3 bucket to store images of ID cards.
3. Create a DynamoDB table: Create a DynamoDB table to store user addresses and S3 URLs of their ID card images.
4. Write the Lambda function in Python3: Write a Python3 function to handle REST API requests, retrieve or store data in DynamoDB and S3, and return responses to the API Gateway.
5. Deploy the Lambda function: Package and deploy the Lambda function to AWS.
6. Create an API Gateway REST endpoint: Create a REST API in API Gateway and connect it to the Lambda function.
7. Create a HTML/JS frontend: Create an HTML/JS-based frontend to allow users to fill in their address information and upload images of their ID cards. The frontend should make REST API calls to the API Gateway to store the data.
8. Test the system: Test the complete system to verify it works as expected.

## Notes

Refer the lambda_function.py file to get an overview of the functionality.
Refer the HTML files to store and retrieve the data
